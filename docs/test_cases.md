# Casos de Prueba — GestorInventario

This document lists the executed test cases and provides Gherkin acceptance scenarios for the QA track. The API contract was previously hand-written; E2E scenarios were scripted with Playwright.

## Test Case Matrix

| ID | Endpoint | Tipo | Input | Esperado |
|----|----------|------|-------|----------|
| TC-API-01 | GET /api/health | Happy | - | 200, {status: ok} |
| TC-API-02 | GET /api/suppliers | Happy | - | 200, lista >=3 |
| TC-API-03 | GET /api/products | Happy | - | 200, lista |
| TC-API-04 | GET /api/products/{id} | Happy | id=1 | 200, campos |
| TC-API-05 | GET /api/products/{id} | Negativo | id=999999 | 404 |
| TC-API-06 | POST /api/products | Happy | body válido | 201 |
| TC-API-07 | POST /api/products | Negativo | SKU duplicado | 409 |
| TC-API-08 | POST /api/products | Negativo | min_stock=-1 | 201 (BUG: sin constraint) |
| TC-API-09 | POST /api/products | Negativo | cost_cents=-1000 | 201 (BUG: sin constraint) |
| TC-API-10 | POST /api/stock/movement | Happy | type=IN, qty=5 | 201, stock +=5 |
| TC-API-11 | POST /api/stock/movement | Edge | qty=2.5 | 201 (BUG: decimal) |
| TC-API-12 | POST /api/stock/movement | Negativo | tipo inválido | 400 |
| TC-API-13 | POST /api/stock/movement | Negativo | producto inexistente | 404 |
| TC-API-14 | GET /api/stock/alerts | Happy | env limpio | 200, lista |
| TC-API-15 | GET /api/stock/alerts | Fallo | ALERTS_FAIL=1 | 503 |
| TC-E2E-01 | UI homepage | Happy | - | Carga tabla productos |
| TC-E2E-02 | UI register movement | Happy | IN/OUT desde UI | Cambia stock visto |
| TC-E2E-03 | UI alerts refresh | Happy | click botón | Actualiza tabla alertas |
| TC-E2E-04 | UI alert fallback | Happy | endpoint filtrado | Muestra error 503 |

## Gherkin Scenarios

| Scenario | Type | Notes |
|----------|------|-------|
| Homepage lists seeded products | Smoke | Verify static index renders product rows |
| User registers IN movement via UI | Functional | Input type=IN, expect stock increase |
| User registers OUT movement via UI | Functional | Input type=OUT, expect stock decrease |
| Stock below min triggers alert badge | Regression | Row styling updates after movement |
| Alert service 503 message in UI | Negative | Error banner shown, page not crashed |
| Decimal qty accepted by backend | Negative | Accepted due to schema-defined float |
| Negative stock allowed | Negative | Triggered when OUT qty exceeds stock |

### Gherkin examples

Feature: Movimientos de stock desde interfaz

  Scenario: Aumento de stock desde la UI
    Given la home de Gestor Inventario está cargada
    When registro un movimiento tipo IN con qty 3
    Then veo el stock actualizado y un mensaje OK

Feature: Alertas de stock mínimo desde frontend

  Scenario: Refresco de alertas desde la UI
    Given la lista de productos está visible
    And menos de 5 productos tienen stock, incluyendo el seleccionado
    When hago click en "Consultar alertas"
    Then la tabla de alertas se actualiza o muestra "Sin alertas"
    And no se lanza una excepción al usuario

Feature: Validación negativa backend

  Scenario: Fallo simulado del servicio de alertas
    When consulto /api/stock/alerts bajo ALERTS_FAIL=1
    Then el API devuelve 503
    But la UI sigue funcionando
