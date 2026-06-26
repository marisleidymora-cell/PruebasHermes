# Reporte de Defectos - Track QA Reto AI-First Fase 1

**SUT:** gestor-inventario (FastAPI + SQLite)
**Fecha:** 2026-06-25
**Agente:** OWL (Hermes Agent)

---

## Defect #1 - Stock Negativo Permitido

| Campo | Detalle |
|-------|---------|
| **ID** | BUG-001 |
| **Severidad** | CRÍTICA |
| **Endpoint** | `POST /api/stock/movement` (type=OUT) |
| **Estado** | Confirmado (test `test_defect_negative_stock_allowed`) |

### Descripción
La API permite registrar movimientos de salida (OUT) con cantidad mayor al stock disponible. El stock resultante es negativo, violando una invariante de negocio fundamental.

### Impacto
- Inventario con stock negativo es una inconsistencia de negocio
- Reportes de inventario serán incorrectos
- Operaciones downstream pueden fallar por datos inválidos

### Pasos de Reproducción
```python
# Producto 1 tiene stock inicial de 50
POST /api/stock/movement
{
    "product_id": 1,
    "type": "OUT",
    "qty": 99999,
    "notes": "Test negativo"
}

# Respuesta: 201 Created
# Stock resultante: -99949
```

### Rechazo Esperado
Debería retornar HTTP 400 con mensaje como "Stock insuficiente" o "Cantidad excede stock disponible".

---

## Defect #2 - Cantidad Decimal Aceptada

| Campo | Detalle |
|-------|---------|
| **ID** | BUG-002 |
| **Severidad** | ALTA |
| **Endpoint** | `POST /api/stock/movement` |
| **Estado** | Confirmado (test `test_defect_decimal_quantity_accepted`) |

### Descripción
El campo `qty` en los movimientos de stock acepta valores decimales (float) cuando debería ser entero. La columna SQLite está definida como REAL.

### Impacto
- Inventario con cantidades fraccionarias no tiene sentido para productos unitarios
- Cálculos de stock pueden acumular errores de precisión
- Inconsistencia con el modelo de dominio (no se pueden tener 2.5 unidades de un producto de oficina)

### Pasos de Reproducción
```python
POST /api/stock/movement
{
    "product_id": 1,
    "type": "IN",
    "qty": 2.5,
    "notes": "Test decimal"
}

# Respuesta: 201 Created
# qty almacenado: 2.5
```

### Rechazo Esperado
Debería retornar HTTP 400 indicando que qty debe ser un número entero.

---

## Defect #3 - min_stock Negativo Permitido

| Campo | Detalle |
|-------|---------|
| **ID** | BUG-003 |
| **Severidad** | MEDIA |
| **Endpoint** | `POST /api/products` |
| **Estado** | Confirmado (test `test_defect_negative_min_stock_accepted`) |

### Descripción
Se permite crear productos con `min_stock` negativo sin validación. Esto hace que las alertas de stock bajo nunca se disparen para ese producto.

### Impacto
- Las alertas de stock bajo serán inútiles para productos con min_stock negativo
- Riesgo de quedar sin stock sin notificación
- Degradación de la funcionalidad principal del sistema

### Pasos de Reproducción
```python
POST /api/products
{
    "name": "Producto con min_stock negativo",
    "sku": "NEG-001",
    "cost_cents": 10000,
    "price_cents": 15000,
    "stock": 10,
    "min_stock": -1,
    "supplier_id": 1
}

# Respuesta: 201 Created
# min_stock almacenado: -1
```

### Rechazo Esperado
Debería retornar HTTP 400 indicando que min_stock debe ser >= 0.

---

## Defect #4 - cost_cents Negativo Permitido

| Campo | Detalle |
|-------|---------|
| **ID** | BUG-004 |
| **Severidad** | MEDIA |
| **Endpoint** | `POST /api/products` |
| **Estado** | Confirmado (test `test_defect_negative_cost_accepted`) |

### Descripción
Se permite crear productos con `cost_cents` negativo sin validación. Esto genera datos de costos inconsistentes.

### Impacto
- Reportes financieros incorrectos
- Cálculos de margen de ganancia erróneos
- Posible confusión en facturación

### Pasos de Reproducción
```python
POST /api/products
{
    "name": "Producto con costo negativo",
    "sku": "NEG-002",
    "cost_cents": -5000,
    "price_cents": 15000,
    "stock": 10,
    "min_stock": 5,
    "supplier_id": 1
}

# Respuesta: 201 Created
# cost_cents almacenado: -5000
```

### Rechazo Esperado
Debería retornar HTTP 400 indicando que cost_cents debe ser >= 0.

---

## Resumen de Severidad

| ID | Defecto | Severidad | Test |
|----|---------|-----------|------|
| BUG-001 | Stock Negativo | CRÍTICA | `test_defect_negative_stock_allowed` |
| BUG-002 | Cantidad Decimal | ALTA | `test_defect_decimal_quantity_accepted` |
| BUG-003 | min_stock Negativo | MEDIA | `test_defect_negative_min_stock_accepted` |
| BUG-004 | cost_cents Negativo | MEDIA | `test_defect_negative_cost_accepted` |

---

## Cobertura de Pruebas

| Dimensión | Tests | Resultado |
|-----------|-------|-----------|
| API Contract (status codes) | 5 | 100% pasados |
| Functional Happy Path | 3 | 100% pasados |
| Defect Detection | 4 | 100% pasados (detectan bugs) |
| Integration Failure (ALERTS_FAIL) | 2 | 100% pasados |
| Data Integrity | 2 | 100% pasados |
| **Total API** | **16** | **100%** |
| E2E UI Tests | 4 | 100% pasados |
| **Total E2E** | **4** | **100%** |

---

## Notas Técnicas

- Los tests API usan `ASGITransport` de httpx para testing sin servidor real
- Los tests E2E levantan el servidor en puerto 8001 con base de datos aislada
- Cada test usa `DB_PATH=/tmp/test_inventario.db` para aislamiento total
- El fixture `autouse` reinicia la base de datos antes de cada test
