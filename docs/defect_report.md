# Reporte de Defectos
Qué hay: defectos confirmados con severidad, pasos de repro y vínculo a evidencia automatizada.

## Resumen
Se registran hallazgos basados en ejecución real del SUT en `localhost:8000` en modo normal (`ALERTS_FAIL` sin activar).

### D-01: Stock negativo permitido
- Severidad: Alta
- Escenario: `POST /api/stock/movement` con `type=OUT` y `qty=99999` (excede stock disponible)
- Resultado: 201 y el stock queda negativo
- Evidencia: respuesta HTTP 201 + valor negativo en `GET /api/products/{id}`

### D-02: Cantidad decimal aceptada
- Severidad: Media
- Escenario: `POST /api/stock/movement` con `qty=1.5`
- Resultado: 201 y movimiento registrado con `qty=1.5`
- Evidencia: respuesta HTTP 201 y cuerpo con `qty=1.5`

### D-03: Validaciones faltantes en producto
- Severidad: Media
- Escenario: `POST /api/products` con `min_stock=-1` y `cost_cents=-1000`
- Resultado: 201 (no hay validación de negativos)
- Evidencia: respuesta HTTP 201 y valores persistidos

### D-04: Simulación de fallo de alertas depende de arranque con ALERTS_FAIL=1
- Severidad: Hallazgo de entorno (no bloqueante)
- Escenario: `GET /api/stock/alerts` con la variable `ALERTS_FAIL=1` activa
- Resultado: si el SUT ya está corriendo sin esa variable, activarla no cambia el comportamiento en caliente;
  la instancia debe arrancarse con `ALERTS_FAIL=1` desde el inicio para que el endpoint responda 503.
- Evidencia: `tests/e2e/test_ui_registration_and_alerts.py::test_alerts_section_shows_503_when_alert_service_down`
  y `tests/api/test_stock_movements.py::TestAlerts::test_alerts_with_alerts_fail_returns_503` levantan un
  servidor auxiliar propio con `ALERTS_FAIL=1` desde el arranque y confirman 503 real. Tests pasan en verde.
- Riesgo residual: esos tests dependen de una ruta local fija al SUT
  (`~/Desktop/reto-ai-first-fase1/reto-ai-first-fase1/3-challenge/gestor-inventario`); si esa carpeta cambia
  de ubicación, el aislamiento del servidor auxiliar deja de funcionar.

### D-05: qty negativo invierte la dirección del movimiento sin validación
- Severidad: Media
- Escenario: `POST /api/stock/movement` con `type=IN` y `qty=-5`
- Resultado: 201, y el stock del producto disminuye en vez de aumentar (un IN con qty negativo
  se comporta como un OUT). El endpoint solo valida `type` (IN/OUT), no el signo de `qty`.
- Evidencia: `tests/api/test_stock_movements.py::TestMovementQtyBoundaries::test_movement_with_negative_qty_is_accepted_and_inverts_direction`

### D-06: qty=0 se acepta y registra un movimiento sin efecto
- Severidad: Baja
- Escenario: `POST /api/stock/movement` con `qty=0`
- Resultado: 201, se guarda un registro en el historial de movimientos, pero el stock no cambia.
  No es un error funcional grave, pero ensucia el historial con movimientos "vacíos" sin que el
  usuario reciba ninguna advertencia.
- Evidencia: `tests/api/test_stock_movements.py::TestMovementQtyBoundaries::test_movement_with_qty_zero_is_accepted_no_op`

Nota: la suite API valida estos caminos para dejar evidencia reproducible de los defectos.
