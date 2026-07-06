# Casos de prueba — Gestor de Inventario (Gherkin)

Feature: Gestión de inventario
  Como usuario del sistema
  Quiero gestionar productos, movimientos de stock y alertas
  Para mantener el inventario actualizado y controlado

Background:
  Given la API está disponible en "http://127.0.0.1:8000"
  And la base de datos está inicializada con datos de prueba

# ===================== BACKEND API [BE] =====================

## Happy Path

Scenario: T-[BE][HP] Health check
  Given el servicio está corriendo
  When realizo una petición GET a "/api/health"
  Then recibo un código de respuesta 200
  And el cuerpo contiene {"status":"ok"}

Scenario: T-[BE][HP] Listado de proveedores seed
  When realizo una petición GET a "/api/suppliers"
  Then recibo un código de respuesta 200
  And la respuesta contiene exactamente 3 registros

Scenario: T-[BE][HP] Listado de productos seed
  When realizo una petición GET a "/api/products"
  Then recibo un código de respuesta 200
  And la respuesta contiene exactamente 6 registros
  And los SKUs incluyen "PAP-001", "TON-002", "SIL-003", "MON-004", "TEC-005", "MOU-006"

Scenario: T-[BE][HP] Movimiento IN aumenta stock
  Given el producto con id 1 tiene stock 50
  When realizo una petición POST a "/api/stock/movement" con body {"product_id":1,"type":"IN","qty":10}
  Then recibo un código de respuesta 201
  And el stock del producto 1 es 60

Scenario: T-[BE][HP] Movimiento OUT reduce stock
  Given el producto con id 2 tiene stock 12
  When realizo una petición POST a "/api/stock/movement" con body {"product_id":2,"type":"OUT","qty":3}
  Then recibo un código de respuesta 201
  And el stock del producto 2 es 9

Scenario: T-[BE][HP] Listado de alertas de stock
  Given existe un producto con stock 1 y min_stock 2
  When realizo una petición GET a "/api/stock/alerts"
  Then recibo un código de respuesta 200
  And la respuesta incluye el producto con stock bajo

Scenario: T-[BE][HP] Historial de movimientos
  When realizo una petición GET a "/api/movements"
  Then recibo un código de respuesta 200
  And la respuesta es una lista con al menos 1 registro

Scenario: T-[BE][HP] Alta de producto exitosa
  When realizo una petición POST a "/api/products" con un payload válido
  Then recibo un código de respuesta 201
  And el cuerpo contiene el sku "NEW-001"
  And el stock inicial es 10

Scenario: T-[BE][HP] Movimiento OUT registra cantidad y notas
  When realizo una petición POST a "/api/stock/movement" con body {"product_id":1,"type":"OUT","qty":1,"notes":"sale"}
  Then recibo un código de respuesta 201
  And el cuerpo contiene type "OUT", qty 1 y notes "sale"

## Negativos y Edge

Scenario: T-[BE][NG] Alta de producto duplicado SKU
  When realizo una petición POST a "/api/products" con sku "PAP-001"
  Then recibo un código de respuesta 409

Scenario: T-[BE][NG] Alta de producto con proveedor inexistente
  When realizo una petición POST a "/api/products" con supplier_id 999
  Then recibo un código de respuesta 400

Scenario: T-[BE][NG] Alta de producto con campos inválidos
  When realizo una petición POST a "/api/products" con campos vacíos o negativos
  Then recibo un código de respuesta 422 o 400

Scenario: T-[BE][NG] Movimiento con tipo inválido
  When realizo una petición POST a "/api/stock/movement" con body {"product_id":1,"type":"BAD","qty":1}
  Then recibo un código de respuesta 400

Scenario: T-[BE][NG] Movimiento a producto inexistente
  When realizo una petición POST a "/api/stock/movement" con body {"product_id":999,"type":"IN","qty":1}
  Then recibo un código de respuesta 404

Scenario: T-[BE][NG] Producto no encontrado por ID
  When realizo una petición GET a "/api/products/999"
  Then recibo un código de respuesta 404

Scenario: T-[BE][NG] Simulación de fallo en alertas
  Given la variable ALERTS_FAIL está establecida en 1
  When realizo una petición GET a "/api/stock/alerts"
  Then recibo un código de respuesta 503

Scenario: T-[BE][NG] Fallo de alertas propaga en movimiento OUT
  Given la variable ALERTS_FAIL está establecida en 1
  When realizo una petición POST a "/api/stock/movement" con body {"product_id":1,"type":"OUT","qty":1}
  Then recibo un código de respuesta 503

Scenario: T-[BE][NG] Movimiento OUT con cantidad mayor al stock
  When realizo una petición POST a "/api/stock/movement" con qty mayor al stock disponible
  Then recibo un código de respuesta ideal 400
  And el stock no queda negativo

Scenario: T-[BE][NG] Movimiento OUT con cantidad decimal
  When realizo una petición POST a "/api/stock/movement" con qty 1.5
  Then recibo un código de respuesta ideal 400
  And solo se permiten cantidades enteras

# ===================== FRONTEND E2E [FE] =====================

Scenario: T-[FE][HP] Página principal carga correctamente
  Given el navegador abre la URL "http://127.0.0.1:8000/"
  When la página carga completamente
  Then el título contiene "Gestor de Inventario"
  And se muestra una tabla con productos

Scenario: T-[FE][HP] Envío de movimiento desde formulario
  Given estoy en la página principal
  When selecciono el producto 1, tipo IN, cantidad 5 y envío el formulario
  Then la respuesta es 201
  And la tabla de productos se actualiza

Scenario: T-[FE][HP] Consulta de alertas desde interfaz
  Given estoy en la página principal
  When presiono el botón de refrescar alertas
  Then se muestran los productos con stock por debajo del mínimo
