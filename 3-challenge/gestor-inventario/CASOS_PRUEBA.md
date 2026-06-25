# Casos de Prueba -- Gestor de Inventario

## Leyenda
- P = Pasado
- F = Fallido
- N/A = No aplicable (depende de ALERTS_FAIL)

---

## 1. HEALTH

| ID | Nombre | Tipo | Endpoint | Expected | Status |
|----|--------|------|----------|----------|--------|
| TC-001 | Health OK | Happy | GET /api/health | 200 {"status":"ok"} | P |

---

## 2. SUPPLIERS

| ID | Nombre | Tipo | Endpoint | Expected | Status |
|----|--------|------|----------|----------|--------|
| TC-002 | Listar proveedores | Happy | GET /api/suppliers | 200, lista con >=3 | P |
| TC-003 | Campos requeridos | Contrato | GET /api/suppliers | Cada item tiene id,name,email,phone,active | P |
| TC-004 | Orden por ID | Contrato | GET /api/suppliers | ids ascendente | P |

---

## 3. PRODUCTS

| ID | Nombre | Tipo | Endpoint | Expected | Status |
|----|--------|------|----------|----------|--------|
| TC-005 | Listar productos | Happy | GET /api/products | 200, lista con >=6 | P |
| TC-006 | Campos requeridos | Contrato | GET /api/products | Todos los campos presentes | P |
| TC-007 | Precio >= Costo | Negocio | GET /api/products | price_cents >= cost_cents | P |
| TC-008 | Get producto por ID | Happy | GET /api/products/{id} | 200, id coincide | P |
| TC-009 | Producto no encontrado | Negativo | GET /api/products/999999 | 404 | P |
| TC-010 | Crear producto | Happy | POST /api/products | 201, datos correctos | P |
| TC-011 | SKU duplicado | Negativo | POST /api/products | 409 "SKU ya existe" | P |
| TC-012 | Supplier invalido | Negativo | POST /api/products | 400 "Proveedor" | P |
| TC-013 | Campo faltante | Negativo | POST /api/products | 422 | P |

---

## 4. STOCK MOVEMENTS

| ID | Nombre | Tipo | Endpoint | Expected | Status |
|----|--------|------|----------|----------|--------|
| TC-014 | Entrada stock | Happy | POST /api/stock/movement IN | 201, stock +qty | P |
| TC-015 | Salida stock | Happy | POST /api/stock/movement OUT | 201 o 503 (ALERTS_FAIL) | P |
| TC-016 | Tipo invalido | Negativo | POST /api/stock/movement | 400 | P |
| TC-017 | Producto no existe | Negativo | POST /api/stock/movement | 404 | P |
| TC-018 | Stock negativo (BUG) | Bug | POST OUT qty=9999 | 201 (deberia ser 400) | P |
| TC-019 | Cantidad decimal (BUG) | Bug | POST qty=2.5 | 201 (deberia ser 422) | P |
| TC-020 | Estructura respuesta | Contrato | POST /api/stock/movement | id,product_id,type,qty,created_at | P |

---

## 5. STOCK ALERTS

| ID | Nombre | Tipo | Endpoint | Expected | Status |
|----|--------|------|----------|----------|--------|
| TC-021 | Estado alertas | Happy | GET /api/stock/alerts | 200 o 503 | P |
| TC-022 | Estructura alertas | Contrato | GET /api/stock/alerts | id,sku,name,stock,min_stock | P |

---

## 6. MOVEMENTS HISTORY

| ID | Nombre | Tipo | Endpoint | Expected | Status |
|----|--------|------|----------|----------|--------|
| TC-023 | Listar historial | Happy | GET /api/movements | 200, lista | P |
| TC-024 | Movimiento en historial | Happy | POST + GET /api/movements | Movimiento aparece | P |
| TC-025 | Orden descendiente | Contrato | GET /api/movements | ids desc | P |

---

## 7. INTEGRACION

| ID | Nombre | Tipo | Endpoint | Expected | Status |
|----|--------|------|----------|----------|--------|
| TC-026 | Ciclo completo producto | E2E | POST products + movements | Stock correcto | P |
| TC-027 | Multiples entradas | E2E | 3x POST IN qty=10 | stock +30 | P |
| TC-028 | Integridad referencial | Datos | GET suppliers + products | supplier_id valido | P |

---

## Resumen
- Total: 28 casos de prueba
- Pasados: 28
- Fallados: 0
- Bugs encontrados: 3 (DEF-001, DEF-002, DEF-003)
