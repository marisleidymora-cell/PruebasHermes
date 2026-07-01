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

Nota: laSuite API valida estos caminos para dejar evidencia reproducible de los defectos.
