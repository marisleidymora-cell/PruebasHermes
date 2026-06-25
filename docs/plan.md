# Plan de Pruebas — GestorInventario

## Estrategia
- Pruebas de API sobre endpoints REST en `http://localhost:8000`.
- Suite API: `pytest + httpx`.
- Pruebas E2E: Playwright para flujos de UI.

## Alcance
- Contrato de API (status codes y shapes)
- Funcional (happy path, edge, negativos)
- Integridad de datos (stock post-movimiento)
- Fallo de integración (`ALERTS_FAIL=1`)
- E2E (mock)

## Riesgos
- El SUT usa SQLite y se crea en tiempo de ejecución.
- Requiere raise 503 con `ALERTS_FAIL=1`.

## Criterios de aceptación
- Suite API cubre obligatoriamente: health, suppliers, products, movements, alerts.
- Defectos detectados: stock negativo, qty decimal, min_stock negativo, cost_cents negativo.
