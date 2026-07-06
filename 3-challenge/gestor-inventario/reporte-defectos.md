# Reporte de defectos — Gestor de Inventario

## D-01 | qty acepta decimales en movimientos de stock
- Severidad: Media
- Hallazgo: `POST /api/stock/movement` acepta `qty` float y persista en BD sin truncar ni rechazar.
- Pasos:
  1. `POST /api/stock/movement` con `product_id=1`, `type=OUT`, `qty=1.5`
  2. Observar respuesta 201 y campo `qty=1.5`
- Evidencia: suite API incluye caso edge `API-11`
- Impacto: inconsistencias en inventario si se requiere stock entero.

## D-02 | OUT permite stock negativo
- Severidad: Alta
- Hallazgo: No existe validación `qty <= stock`; se puede dejar stock en negativo.
- Pasos:
  1. Elegir producto con stock bajo
  2. `POST /api/stock/movement` con `type=OUT` y `qty > stock`
- Evidencia: respuesta 201 y stock negativo en BD
- Impacto: operativa inválida y posibles alertas falsas.

## D-03 | /api/stock/alerts no expone sku en respuesta documentable
- Severidad: Baja
- Hallazgo: respuesta confirmada incluye filtración, pero se requieren aserciones estables por nombre/campos.
- Pasos: consultar endpoint con producto bajo stock y revisar campos JSON.
- Evidencia: ticket QA interno
