# Reporte de Defectos — gestor-inventario

## DEF-01: Stock negativo permitido
- Severidad: Alta
- Hallazgo: `POST /api/stock/movement` con `type=OUT` y `qty > stock` acepta y deja stock negativo.
- Repro:
  1. `GET /api/products/1` -> stock 50
  2. `POST /api/stock/movement` product_id=1 type=OUT qty=60
  3. `GET /api/products/1` -> stock -10
- Evidencia: Test suite `tests_api.py::TestStockMovements::test_negative_stock_after_out_movement` pasa.

## DEF-02: Cantidades decimales aceptadas
- Severidad: Media
- Hallazgo: `qty` acepta `float` (`2.5`) y se persiste sin rechazo.
- Repro:
  1. `POST /api/stock/movement` product_id=1 type=IN qty=2.5
  2. Response 201 y body `qty=2.5`
- Evidencia: `test_decimal_qty_is_accepted`.

## DEF-03: min_stock sin validación negativa
- Severidad: Media
- Hallazgo: `POST /api/products` acepta `min_stock=-1` y la alerta nunca dispara.
- Repro:
  1. Crear producto con `min_stock=-1`
  2. Bajar stock a 0
  3. `GET /api/stock/alerts` no incluye el producto
- Evidencia: No ejecutado en suite actual; queda como prueba complementaria.

## DEF-04: cost_cents sin validación negativa
- Severidad: Media
- Hallazgo: `POST /api/products` acepta `cost_cents=-1000`.
- Repro:
  1. Crear producto con `cost_cents=-1000`
  2. Valor persiste en DB
- Evidencia: No ejecutado en suite actual; queda como prueba complementaria.

## DEF-05: Integración ALERTS_FAIL=1
- Severidad: Alta
- Hallazgo: Cuando `ALERTS_FAIL=1`, `/api/stock/alerts` y `POST /api/stock/movement` (OUT) retornan 503.
- Repro:
  1. `ALERTS_FAIL=1`
  2. `GET /api/stock/alerts` -> 503
  3. `POST /api/stock/movement` type=OUT -> 503
- Evidencia: `TestIntegrationFailures`.
