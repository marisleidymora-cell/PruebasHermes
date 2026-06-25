# Reporte de Defectos -- Gestor de Inventario

Fecha: 25 Jun 2026
SUT: gestor-inventario v1.0.0
Probador: Hermes Agent (QA AI-First)
Ambiente: Local (uvicorn :8000, SQLite, ALERTS_FAIL=1)

---

## Resumen Ejecutivo

| Severidad | Cantidad |
|-----------|----------|
| ALTA | 2 |
| MEDIA | 1 |
| BAJA | 0 |
| **Total** | **3** |

---

## DEF-001: Stock puede quedar negativo tras movimiento OUT

**Severidad:** ALTA
**Componente:** POST /api/stock/movement
**Asignado a:** Dev team

### Descripcion
El endpoint de movimientos de stock tipo OUT no valida que la cantidad solicitada no exceda el stock disponible. Es posible realizar una salida de 9999 unidades aunque el producto solo tenga 10 en stock, resultando en stock negativo.

### Pasos de Reproduccion
1. Crear producto con stock = 10
2. POST /api/stock/movement con payload: {"product_id": X, "type": "OUT", "qty": 9999}
3. GET /api/products/{X} -> stock = -9989

### Comportamiento Actual
- HTTP 201 Created
- Stock actualizado a valor negativo

### Comportamiento Esperado
- HTTP 400 Bad Request
- Mensaje: "Stock insuficiente"
- Stock no se modifica

### Evidencia
```
POST /api/stock/movement {"product_id": 1, "type": "OUT", "qty": 9999}
-> 201 {"id": 1, "product_id": 1, "type": "OUT", "qty": 9999, ...}

GET /api/products/1
-> {"stock": -9979, ...}
```

### Impacto
Criticidad alta: afecta integridad de datos del inventario. Un vendedor puede "vender" productos que no existen.

---

## DEF-002: Cantidades decimales aceptadas en movimientos

**Severidad:** MEDIA
**Componente:** POST /api/stock/movement (modelo StockMovementIn)
**Asignado a:** Dev team

### Descripcion
El campo `qty` en el modelo `StockMovementIn` esta definido como `float` en lugar de `int`, lo que permite valores decimales como 2.5 unidades. En un contexto de inventario fisico, no tiene sentido medio unidad de un producto.

### Pasos de Reproduccion
1. POST /api/stock/movement con payload: {"product_id": 1, "type": "IN", "qty": 2.5}
2. Verificar respuesta

### Comportamiento Actual
- HTTP 201 Created
- qty almacenado como 2.5

### Comportamiento Esperado
- HTTP 422 Validation Error
- qty debe ser integer positivo

### Evidencia
```
POST /api/stock/movement {"product_id": 1, "type": "IN", "qty": 2.5}
-> 201 {"id": 2, "product_id": 1, "type": "IN", "qty": 2.5, ...}
```

### Impacto
Media: puede causar inconsistencias en conteos de inventario y problemas con productos que no son divisibles.

---

## DEF-003: Acoplamiento entre movimientos y servicio de alertas

**Severidad:** ALTA
**Componente:** POST /api/stock/movement (OUT) + alert_service()
**Asignado a:** Dev team

### Descripcion
Cuando ALERTS_FAIL=1, cualquier movimiento de tipo OUT retorna 503 Service Unavailable, aun cuando el movimiento en si es valido. El servicio de alertas es un efecto secundario que no deberia impedir la operacion principal de stock.

### Pasos de Reproduccion
1. Servidor corriendo con ALERTS_FAIL=1
2. POST /api/stock/movement con type OUT valido

### Comportamiento Actual
- HTTP 503 Service Unavailable
- Mensaje: "Servicio de alertas no disponible"
- Movimiento NO se persiste

### Comportamiento Esperado
- HTTP 201 Created
- Movimiento se completa
- Alerta falla silenciosamente o se maneja async

### Evidencia
```
POST /api/stock/movement {"product_id": 1, "type": "OUT", "qty": 1}
-> 503 {"detail": "Servicio de alertas no disponible"}
```

### Impacto
Criticidad alta: el servicio de alertas (feature secundario) bloquea operaciones de stock criticas. En produccion, caida del servicio de alertas detendria todas las ventas.

---

## Recomendaciones

1. DEF-001: Agregar validacion `if delta < 0 and abs(delta) > product["stock"]` antes de actualizar
2. DEF-002: Cambiar `qty: float` a `qty: int` en StockMovementIn
3. DEF-003: Separar la logica de alertas del movimiento principal (async/circuit breaker)

---

## Trazabilidad

| Defecto | Test ID | Archivo |
|---------|---------|---------|
| DEF-001 | TC-018 | tests/test_api.py::TestStockMovements::test_movement_negative_stock_bug |
| DEF-002 | TC-019 | tests/test_api.py::TestStockMovements::test_movement_float_qty_bug |
| DEF-003 | TC-015 | tests/test_api.py::TestStockMovements::test_movement_out |
