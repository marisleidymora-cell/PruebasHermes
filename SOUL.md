# SOUL.md - PruebasHermes (Track QA)

## Proyecto probado
- SUT: `gestor-inventario` (FastAPI + SQLite + frontend estático)
- Repo base: `reto-ai-first-fase1/3-challenge/gestor-inventario`

## Estrategia
- API contract + funcional + integridad
- E2E con Playwright headed contra Chromium
- Ambiente: servidor local en `http://localhost:8000`
- Ejecución: `pytest` con `httpx` contra el SUT
- Modo ejecutado: SIN `ALERTS_FAIL=1` (ruta feliz) y con intento controlado de 503
- Reportes: Allure integrado; se limpia `allure-results/` al inicio y sirve HTML con `allure serve`

## Herramientas
- Python 3.12 / 3.11
- pytest 9.1.1 + httpx 0.28.1
- Playwright Chromium 1223
- allure-pytest + allure CLI
- uvicorn para levantar el SUT
- curl para diagnosis rápida

## Hallazgos observados (con evidencia)
1. `POST /api/stock/movement` con `type=OUT` y `qty > stock` → genera stock negativo.
2. `POST /api/stock/movement` acepta `qty` decimal (`1.5`) y la registra.
3. `POST /api/products` acepta `min_stock=-1` y `cost_cents=-1000` sin error.
4. Con `ALERTS_FAIL=1` configurado, `GET /api/stock/alerts` sigue devolviendo 200 en lugar de 503.
   - Impacto: impide cerrar la prueba E2E `test_alerts_section_shows_503_when_alert_service_down`.
   - Clasificación: comportamiento observable / hallazgo de alineación entre contrato esperado e implementación.

## Uso de Hermes
- Generación y limpieza inicial de la rama `yeraldine`.
- Generación de casos de prueba, plan de pruebas y documentación QA.
- Ejecución automatizada de suites API y E2E.

## Estado de entregables
- `docs/test_cases.md`: alineado 1 a 1 con la suite en código.
- `docs/plan.md`: actualizado con alcance, riesgos y criterios de aceptación.
- `docs/historial_sesiones.md`: actualizado con resultados de ejecución y hallazgo 503.

## Issues / Bloqueos
- Acceso a GitHub: resuelto con `gh auth login`.
- Escenario 503 desde UI (E2E): no cerrado porque el comportamiento del SUT no replica
  el fallo simulado documentado en la guía del reto.
