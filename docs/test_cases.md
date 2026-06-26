# Casos de Prueba — GestorInventario
Correspondencia directa con la suite automatizada en `tests/`.

## Resumen de cobertura real

- API: 18 pruebas en `tests/api`.
- E2E: 6 pruebas verdes en `tests/e2e` (`tests/e2e/test_playwright_suite.py`).
- Pendiente de cierre: 1 prueba E2E en `tests/e2e/test_ui_registration_and_alerts.py` atada al escenario 503.

limitación confirmada: con `ALERTS_FAIL=1`, `GET /api/stock/alerts` sigue devolviendo 200 en la instancia del SUT en uso, por lo que el escenario 503 desde UI queda como hallazgo/comportamiento no reproducible en este entorno.

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

### tests/e2e/test_playwright_suite.py
- TC-E2E-01 | UI homepage | Happy | - | Carga contenido
- TC-E2E-02 | UI lista productos | Happy | - | Producto seed visible
- TC-E2E-03 | UI alert flow | Happy | - | Accede a home

### tests/e2e/test_ui_registration_and_alerts.py
- TC-E2E-04 | UI movimiento + alertas | Happy | - | Flujo IN/OUT + refresh alertas
- TC-E2E-05 | UI alert 503 | Negativo | ALERTS_FAIL=1 | Pendiente por comportamiento SUT

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
