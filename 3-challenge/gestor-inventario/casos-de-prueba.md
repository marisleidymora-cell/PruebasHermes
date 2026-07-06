# Casos de prueba — Gestor de Inventario

## Backend API

| ID | Módulo | Caso | Tipo | Pasos | Resultado esperado |
|---|---|---|---|---|---|
| API-01 | Health | Health check | Happy | GET `/api/health` | 200 + `{"status":"ok"}` |
| API-02 | Suppliers | Listado proveedores seed | Happy | GET `/api/suppliers` | 200 + 3 registros |
| API-03 | Products | Listado productos seed | Happy | GET `/api/products` | 200 + 6 registros |
| API-04 | Products | Alta producto duplicado SKU | Negativo | POST `/api/products` con `sku="PAP-001"` | 409 |
| API-05 | Products | Alta producto proveedor inexistente | Negativo | POST `/api/products` con `supplier_id=999` | 400 |
| API-06 | Products | Alta producto campos inválidos | Negativo | Campos vacíos o negativos | 422/400 |
| API-07 | Movements | Tipo de movimiento inválido | Negativo | `type="BAD"` | 400 |
| API-08 | Movements | Producto inexistente | Negativo | `product_id=999` | 404 |
| API-09 | Movements | Movimiento IN aumenta stock | Happy | IN `qty=10` sobre producto con stock 50 | Stock 60 + 201 |
| API-10 | Movements | Movimiento OUT reduce stock | Happy | OUT `qty=3` sobre stock 12 | Stock 9 + 201 |
| API-11 | Movements | OUT con qty decimal | Edge/Bug | `qty=1.5` | Acepta hoy; deseo ideal: 400 |
| API-12 | Movements | OUT sin saldo | Negativo | `qty` mayor al stock actual | Hoy 201; deseo ideal: 400 |
| API-13 | Alerts | Listado alertas normal | Happy | Producto `stock <= min_stock` | Aparece en `/api/stock/alerts` |
| API-14 | Alerts | Simulación fallo alertas | Negativo | `ALERTS_FAIL=1` → GET alerts | 503 |
| API-15 | Alerts | Fallo alertas propaga en OUT | Negativo | `ALERTS_FAIL=1` → OUT | 503 |
| API-16 | Movements | Historial de movimientos | Happy | GET `/api/movements` | 200 + lista con registros |
| API-17 | Products | Producto no encontrado | Negativo | GET `/api/products/999` | 404 |
| API-18 | Products | Alta producto exitosa | Happy | POST válido | 201 + campos correctos |
| API-19 | Movements | OUT registra qty y notas | Happy | POST OUT con `notes` | 201 + `type`, `qty`, `notes` |

## Frontend E2E

| ID | Módulo | Caso | Tipo | Pasos | Resultado esperado |
|---|---|---|---|---|---|
| WEB-01 | Home | Página carga | Happy | Abrir `/` | 200 + título + tabla productos |
| WEB-02 | Home | Formulario movimiento | Happy | Completar IN y enviar | 201 + tabla recargada |
| WEB-03 | Home | Consulta alertas | Happy | Click en alertas | Muestra productos bajos |
