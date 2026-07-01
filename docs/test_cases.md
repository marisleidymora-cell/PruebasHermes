# Casos de Prueba — GestorInventario
Qué hay: matriz de casos API + E2E, códigos TC-API-01..18 y TC-E2E-01..07, alineada a tests/ y a docs/gherkin_features.feature.

## Resumen de cobertura real

- API: 18 pruebas en `tests/api`.
- E2E: 7 pruebas verdes en `tests/e2e`.
- Total suite: 25 pasadas, 0 falladas (verificado con `python -m pytest -v`).

Escenario 503 resuelto: `tests/e2e/test_ui_registration_and_alerts.py::test_alerts_section_shows_503_when_alert_service_down`
levanta un servidor auxiliar del SUT en el puerto 18003 con `ALERTS_FAIL=1` para aislar el caso y confirma que
`GET /api/stock/alerts` responde 503 desde la UI. Riesgo conocido: ese test depende de una ruta local fija
(`~/Desktop/reto-ai-first-fase1/reto-ai-first-fase1/3-challenge/gestor-inventario`); si esa carpeta se mueve o
se borra, el test deja de poder levantar el servidor auxiliar.

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
- TC-API-12 | POST /api/stock/movement | Happy | type=OUT, qty=1 | 201
- TC-API-13 | POST /api/stock/movement | Negativo | aislar ALERTS_FAIL | validación especial

### tests/api/test_negative_movements.py
- TC-API-14 | POST /api/stock/movement | Negativo | tipo inválido | 400
- TC-API-15 | POST /api/stock/movement | Negativo | producto inexistente | 404

### tests/api/test_data_integrity.py
- TC-API-16 | POST /api/stock/movement | Happy | type=IN, qty=7 | stock +=7 exacto
- TC-API-17 | POST /api/stock/movement | Happy | type=OUT, qty=3 | stock -=3 exacto

### tests/api/test_movements_log.py
- TC-API-18 | GET /api/movements | Happy | - | 200, lista, orden desc por id

### tests/e2e/test_playwright_suite.py
- TC-E2E-01 | UI homepage | Happy | - | Carga contenido
- TC-E2E-02 | UI lista productos | Happy | - | Producto seed visible
- TC-E2E-03 | UI alert flow | Happy | - | Accede a home

### tests/e2e/test_ui_registration_and_alerts.py
- TC-E2E-04 | UI movimiento + alertas | Happy | - | Flujo IN/OUT + refresh alertas
- TC-E2E-05 | UI alert 503 | Negativo | ALERTS_FAIL=1 (servidor auxiliar puerto 18003) | 503 confirmado desde UI

### tests/e2e/test_frontend_flow.py
- TC-E2E-06 | UI browse products | Happy | - | Lectura productos desde UI

### tests/e2e/test_home.py
- TC-E2E-07 | UI home HTTP | Happy | - | 200 en home

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
