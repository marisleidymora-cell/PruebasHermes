@qa @gestor-inventario @api @e2e
Feature: Suite completa de validación QA sobre gestor-inventario

  Como equipo de QA
  Quiero validar API, datos y flujos de UI
  Para confirmar alineación con el contrato y detectar desviaciones

  Background: Servidor SUT levantado
    Given el SUT está disponible en "http://localhost:8000"
    And la base contiene productos y proveedores sembrados

# =============================================================================
# CONTRATO Y CRUD DE PRODUCTOS
# =============================================================================

  @TC-API-01
  Scenario: Health check responde ok
    When consulto GET /api/health
    Then el estado es 200
    And el body tiene status = "ok"

  @TC-API-02
  Scenario: Listado de proveedores
    When consulto GET /api/suppliers
    Then el estado es 200
    And recibo un array con al menos 1 proveedor

  @TC-API-03
  Scenario: Listado de productos
    When consulto GET /api/products
    Then el estado es 200
    And recibo un array con al menos 1 producto

  @TC-API-04
  Scenario: Detalle de producto existente
    When consulto GET /api/products/1
    Then el estado es 200
    And el body contiene los campos id, name, sku, cost_cents, price_cents, stock, min_stock, supplier_id

  @TC-API-05
  Scenario: Producto inexistente
    When consulto GET /api/products/999999
    Then el estado es 404

  @TC-API-06
  Scenario: Crear producto con datos válidos
    When creo un producto con sku único y datos válidos
    Then el estado es 201
    And el producto creado contiene el mismo sku y stock = 100

  @TC-API-07
  Scenario: Crear producto con SKU duplicado
    When intento crear un producto con sku = "PAP-001"
    Then el estado es 409

  @TC-API-08
  Scenario: Crear producto acepta min_stock negativo
    When creo un producto con min_stock = -1
    Then el estado es 201
    And el campo min_stock se persiste sin rechazo
    And es un hallazgo documentado

  @TC-API-09
  Scenario: Crear producto acepta costo negativo
    When creo un producto con cost_cents = -1000
    Then el estado es 201
    And el campo cost_cents se persiste sin rechazo
    And es un hallazgo documentado

  @TC-API-10 @TC-API-16 @TC-API-17
  Scenario: Listado inicial de movimientos
    When consulto GET /api/movements antes de modificar datos
    Then el estado es 200
    And recibo un array
    And el orden puede ser descendente por id si hay más de un movimiento

# =============================================================================
# MOVIMIENTOS Y ALERTAS API
# =============================================================================

  @TC-API-11
  Scenario: Alertas sin fallo devuelven 200
    When consulto GET /api/stock/alerts sin ALERTS_FAIL
    Then el estado es 200
    And recibo un array, posiblemente vacío

  @TC-API-12
  Scenario: Movimiento OUT válido aceptado
    When envío POST /api/stock/movement con product_id=2, type="OUT", qty=1
    Then el estado es 201
    And el movimiento queda registrado

  @TC-API-13
  Scenario: Movimiento con servicio de alertas forzado a fallo
    Given levanto un servidor auxiliar con ALERTS_FAIL=1
    When consulto POST /api/stock/movement en ese servidor con product_id válido
    Then el estado es 201 o 503
    And dejo evidencia del comportamiento frente al fallo aislado

  @TC-API-14
  Scenario: Movimiento con tipo inválido
    When envío POST /api/stock/movement con type="INVALID"
    Then el estado es 400

  @TC-API-15
  Scenario: Movimiento a producto inexistente
    When envío POST /api/stock/movement con product_id=999999
    Then el estado es 404

  @TC-API-16
  Scenario: Movimiento IN aumenta stock exactamente
    Given consulto el stock inicial del producto 1
    When envío POST /api/stock/movement con type="IN", qty=7
    Then el estado es 201
    And el stock final del producto 1 es inicial + 7

  @TC-API-17
  Scenario: Movimiento OUT disminuye stock exactamente
    Given consulto el stock inicial del producto 2
    When envío POST /api/stock/movement con type="OUT", qty=3
    Then el estado es 201
    And el stock final del producto 2 es inicial - 3

# =============================================================================
# E2E - FLUJOS DE UI
# =============================================================================

  @TC-E2E-01
  Scenario: La homepage carga contenido
    When abro la raíz del sitio con el navegador
    Then la página tiene contenido HTML no vacío
    And veo el título "Gestor de Inventario" o el encabezado correspondiente

  @TC-E2E-02
  Scenario: Lista de productos visible en UI
    When abro la página principal
    Then veo al menos un producto sembrado como "Resma Papel Carta" o "PAP-001"

  @TC-E2E-03
  Scenario: Flujo básico de consulta de alertas desde UI
    When abro la home y espero carga completa
    Then la interfaz responde y puedo acceder a la sección de alertas sin excepción

  @TC-E2E-04
  Scenario: Registrar movimiento y ver actualización en UI
    When selecciono producto, tipo="IN" y qty=3
    And confirmo el movimiento
    Then veo mensaje de éxito con "Movimiento" y "Tipo: IN"
    And el stock visible cambia respecto al valor inicial

  @TC-E2E-05
  Scenario: Navegación y productos desde UI
    When abro la UI contra el API backend
    Then GET /api/products responde 200
    And GET /api/products/1 responde 200

  @TC-E2E-06
  Scenario: Home HTTP responde desde frontend
    When consulto la ruta / con cliente HTTP
    Then el estado es 200

  @TC-E2E-07
  Scenario: Sección de alertas con fallo simulado desde UI
    Given levanto un SUT auxiliar con ALERTS_FAIL=1 en puerto 18003
    When abro la UI de ese servidor y hago click en Consultar alertas
    Then la llamada a /api/stock/alerts debe responder 503
    And si el SUT no replica el fallo, se deja como hallazgo de desviación
