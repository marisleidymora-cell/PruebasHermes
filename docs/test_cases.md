# Casos de Prueba — GestorInventario
Qué hay: matriz de casos API + E2E, códigos TC-API-01..20 y TC-E2E-01..05, alineada a tests/ y a docs/gherkin_features.feature.

## Resumen de cobertura real

- API: 21 pruebas en `tests/api` (incluye 2 smoke de frontend reclasificados desde E2E).
- E2E real (navegador): 5 pruebas verdes en `tests/e2e`.
- Total suite: 28 pasadas, 0 falladas — verificado con `python -m pytest -v`, corrido 3 veces
  seguidas sin cambios de resultado (suite repetible, ver nota de aislamiento de datos abajo).

Escenario 503 resuelto: `tests/e2e/test_ui_registration_and_alerts.py::test_alerts_section_shows_503_when_alert_service_down`
levanta un servidor auxiliar del SUT con `ALERTS_FAIL=1` para aislar el caso y confirma que
`GET /api/stock/alerts` responde 503 desde la UI. El mismo mecanismo ahora también se usa desde
la suite de API (`tests/api/test_stock_movements.py`) mediante la fixture `alerts_fail_client`.

Aislamiento de datos: la mayoría de los tests que antes mutaban los productos semilla (id=1, id=2)
ahora usan la fixture `fresh_product`, que crea un producto nuevo por test. Esto hace que la suite
sea repetible: correrla varias veces seguidas no acumula cambios de stock ni afecta a otros tests.

Riesgo conocido: el escenario 503 (API y E2E) depende de una ruta local fija al SUT
(`~/Desktop/reto-ai-first-fase1/reto-ai-first-fase1/3-challenge/gestor-inventario`); si esa carpeta
se mueve o se borra, esos tests dejan de poder levantar su servidor auxiliar.

## Matriz de casos por código

### tests/api/test_api_contract.py
- TC-API-01 | GET /api/health | Happy | - | 200, body dict, status=ok
- TC-API-02 | GET /api/suppliers | Happy | - | 200, lista >= 1
- TC-API-03 | GET /api/products | Happy | - | 200, lista >= 1
- TC-API-04 | GET /api/products/1 | Happy | id=1 | 200, campos requeridos
- TC-API-05 | GET /api/products/999999 | Negativo | id=999999 | 404
- TC-API-06 | POST /api/products | Happy | body válido | 201
- TC-API-07 | POST /api/products | Negativo | SKU duplicado | 409
- TC-API-08 | POST /api/products | Negativo | min_stock=-1 | 201 (BUG)
- TC-API-09 | POST /api/products | Negativo | cost_cents=-1000 | 201 (BUG)
- TC-API-10 | GET /api/movements | Happy | - | 200, lista

### tests/api/test_stock_movements.py
- TC-API-11 | GET /api/stock/alerts | Happy | env limpio | 200, lista
- TC-API-12 | GET /api/stock/alerts | Negativo/Integración | servidor auxiliar ALERTS_FAIL=1 | 503 real confirmado
- TC-API-13 | POST /api/stock/movement (OUT) | Negativo/Integración | servidor auxiliar ALERTS_FAIL=1 | 503 real confirmado
- TC-API-14 | POST /api/stock/movement (OUT) | Happy | fresh_product, qty=1 | 201

### tests/api/test_stock_movements.py — frontera de qty
- TC-API-15 | POST /api/stock/movement (IN) | Frontera | qty=0 | 201, stock sin cambios (BUG/hallazgo)
- TC-API-16 | POST /api/stock/movement (IN) | Frontera | qty=-5 | 201, stock resta en vez de sumar (BUG/hallazgo)

### tests/api/test_negative_movements.py
- TC-API-17 | POST /api/stock/movement | Negativo | tipo inválido | 400
- TC-API-18 | POST /api/stock/movement | Negativo | producto inexistente | 404

### tests/api/test_data_integrity.py
- TC-API-19 | POST /api/stock/movement | Happy | type=IN, qty=7, fresh_product | stock +=7 exacto
- TC-API-20 | POST /api/stock/movement | Happy | type=OUT, qty=3, fresh_product | stock -=3 exacto

### tests/api/test_movements_log.py
- TC-API-21 | GET /api/movements | Happy | - | 200, lista, orden desc por id

### tests/api/test_frontend_smoke.py
(Reclasificado desde E2E: usa httpx, no navegador — ver nota abajo)
- TC-SMOKE-01 | GET / | Happy | - | 200
- TC-SMOKE-02 | GET /api/products, /api/products/1 | Happy | - | 200

### tests/e2e/test_playwright_suite.py
- TC-E2E-01 | UI homepage | Happy | - | Carga contenido
- TC-E2E-02 | UI lista productos | Happy | - | Producto seed visible
- TC-E2E-03 | UI alert flow | Happy | - | Click real en "Consultar alertas", respuesta 200 y sección visible

### tests/e2e/test_ui_registration_and_alerts.py
- TC-E2E-04 | UI movimiento + alertas | Happy | - | Flujo IN/OUT + refresh alertas
- TC-E2E-05 | UI alert 503 | Negativo | ALERTS_FAIL=1 (servidor auxiliar, helper centralizado en conftest.py) | 503 confirmado desde UI

## Nota de reclasificación (E2E real vs smoke de frontend)

Antes existían `tests/e2e/test_home.py` y `tests/e2e/test_frontend_flow.py`, etiquetados como E2E pero
implementados con `httpx` (peticiones HTTP directas), sin abrir ningún navegador. Eso inflaba el conteo
de "pruebas E2E" con pruebas que en realidad eran API. Se movieron a `tests/api/test_frontend_smoke.py`
y se renombraron TC-SMOKE-01/02 para reflejar lo que de verdad hacen. Los únicos códigos TC-E2E-xx que
quedan son pruebas que abren Chromium de verdad con Playwright.

## Gherkin Scenarios vigentes

Feature: Movimientos de stock desde interfaz

  Scenario: Aumento de stock desde la UI
    Given la home está cargada
    When registro IN qty 3
    Then el stock aumenta exactamente 3
    And veo mensaje OK

  Scenario: Disminución de stock desde la UI
    Given la home está cargada
    When registro OUT qty valida
    Then el stock disminuye exactamente esa cantidad
    And veo mensaje OK

Feature: Alertas de stock mínimo desde frontend

  Scenario: Refresco de alertas desde la UI
    Given la lista de productos está visible
    And el servicio de alertas está operativo
    When hago click en Consultar alertas
    Then la sección se actualiza o muestra Sin alertas
    And no se lanza una excepción al usuario

  Scenario: Fallo simulado del servicio de alertas
    When consulto /api/stock/alerts bajo ALERTS_FAIL=1
    Then la API debería devolver 503
    But la UI sigue funcionando sin excepción visible

# =============================================================================
# Trazabilidad a escenarios Gherkin
# =============================================================================
- Todos los casos de prueba anteriores están reflejados en `docs/gherkin_features.feature`.
- Los tags `@TC-...` en el archivo `.feature` se alinean 1 a 1 con los códigos de esta matriz.
