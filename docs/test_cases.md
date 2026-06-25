# Casos de Prueba

| ID | Endpoint | Tipo | Input | Esperado |
|----|----------|------|-------|----------|
| TC-API-01 | GET /api/health | Happy | - | 200 + status ok |
| TC-API-02 | GET /api/suppliers | Happy | - | 200 + lista >=3 |
| TC-API-03 | GET /api/products | Happy | - | 200 + lista |
| TC-API-04 | GET /api/products/{id} | Happy | id=1 | 200 + campos |
| TC-API-05 | GET /api/products/{id} | Negativo | id=999999 | 404 |
| TC-API-06 | POST /api/products | Happy | body valido | 201 |
| TC-API-07 | POST /api/products | Negativo | sku duplicado | 409 |
| TC-API-08 | POST /api/products | Negativo | min_stock=-1 | 201 (BUG: sin constraint) |
| TC-API-09 | POST /api/products | Negativo | cost_cents=-1000 | 201 (BUG: sin constraint) |
| TC-API-10 | POST /api/stock/movement | Happy | type=IN, qty=5 | 201, stock +=5 |
| TC-API-11 | POST /api/stock/movement | Edge | qty=2.5 | 201 (BUG decimal) |
| TC-API-12 | POST /api/stock/movement | Negativo | tipo invalido | 400 |
| TC-API-13 | POST /api/stock/movement | Negativo | producto inexistente | 404 |
| TC-API-14 | GET /api/stock/alerts | Happy | env limpio | 200 + lista |
| TC-API-15 | GET /api/stock/alerts | Fallo | ALERTS_FAIL=1 | 503 |
