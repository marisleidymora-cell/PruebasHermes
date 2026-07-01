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
4. Con `ALERTS_FAIL=1` desde el arranque, `GET /api/stock/alerts` responde 503 correctamente.
   Confirmado con servidor auxiliar propio tanto desde API (`tests/api/test_stock_movements.py`)
   como desde E2E (`tests/e2e/test_ui_registration_and_alerts.py`), reusando el mismo helper
   centralizado en `tests/conftest.py`.
5. `qty=0` en un movimiento se acepta (201) y no cambia el stock, pero sí queda en el historial.
6. `qty` negativo en un movimiento IN se acepta (201) e invierte la dirección: resta stock en vez
   de sumarlo. Ver D-05 y D-06 en `docs/defect_report.md`.

## Uso de Hermes
- Generación y limpieza inicial de la rama `yeraldine`.
- Generación de casos de prueba, plan de pruebas y documentación QA.
- Ejecución automatizada de suites API y E2E.
- Revisión crítica de la suite existente: se detectaron y corrigieron un assert que nunca podía
  fallar, dos "E2E" que en realidad eran smoke de API, falta de aislamiento de datos entre tests,
  y ausencia de casos de frontera para `qty`.

## Estado de entregables
- `docs/test_cases.md`: alineado 1 a 1 con la suite en código (TC-API-01..21, TC-SMOKE-01..02, TC-E2E-01..05).
- `docs/plan.md`: actualizado con alcance, riesgos y criterios de aceptación.
- `docs/historial_sesiones.md`: actualizado con resultados de ejecución (28 passed, 0 failed, x3 corridas).
- `docs/defect_report.md`: incluye D-01 a D-06.

## Issues / Bloqueos
- Acceso a GitHub: resuelto con `gh auth login`.
- Escenario 503 desde UI y desde API: resuelto usando un servidor auxiliar propio con `ALERTS_FAIL=1`;
  queda como riesgo documentado la dependencia de ruta local fija al SUT.
- Aislamiento de datos: resuelto con la fixture `fresh_product`; la suite ahora es repetible.
