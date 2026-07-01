# Plan de Pruebas — GestorInventario
Qué hay: estrategia formal, alcance, riesgos y criterios de aceptación.

## Estrategia
- Pruebas de API sobre endpoints REST en `http://localhost:8000`.
- Suite API: `pytest + httpx`.
- Pruebas E2E: Playwright para flujos de UI contra Chromium headed.
- Estrategia centrada en datos y comportamiento observable, sin tocar el SUT.

## Alcance
- Contrato de API (status codes y shapes)
- Funcional (happy path, edge, negativos)
- Integridad de datos (stock post-movimiento)
- Fallo de integración (`ALERTS_FAIL=1`)
- E2E (UI real, no mock)

## Riesgos
- El SUT usa SQLite y se crea en tiempo de ejecución.
- El escenario `ALERTS_FAIL=1` no garantiza 503 en `/api/stock/alerts` en la instancia evaluada; se registra como hallazgo.

## Criterios de aceptación
- Suite API cubre obligatoriamente: health, suppliers, products, movements, alerts.
- Defectos detectados: stock negativo, qty decimal, min_stock negativo, cost_cents negativo.
- E2E: flujos de UI ejecutados y documentados.
