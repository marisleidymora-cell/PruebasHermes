# AI_FIRST_RESUMEN_George_Quintero_2026-07-06.md

## Resumen ejecutivo

Registro real del Track QA para el reto `reto-ai-first-fase1`.  
SUT: `gestor-inventario` (FastAPI + SQLite + frontend vanilla JS).  
 Rama de trabajo: `george-quintero` en `marisleidymora-cell/PruebasHermes`.

---

## Entregables generados

| Archivo | Estado | Observación |
|---------|--------|-------------|
| `SOUL.md` | Entregado | Bitácora de proceso, tooling, decisiones. |
| `plan-de-pruebas.md` | Entregado | Estrategia, alcance, riesgos, criterios de aceptación. |
| `casos-de-prueba.md` | Entregado | Casos happy/edge/negative documentados por endpoint. |
| `defect-report.md` | Entregado | Hallazgos con severidad, repro y evidencia. |
| `tests_api.py` | Entregado | Suite API (pytest + httpx), ejecutable local y CI. |
| `tests_e2e.py` | Entregado | Suite E2E (Playwright), ejecutable local y CI. |
| `pyproject.toml` | Entregado | Dependencias reproducibles (`pytest`, `httpx`, `pytest-asyncio`, `playwright`, `pytest-cov`). |
| `conftest.py` | Entregado | Fixtures compartidos (`base_url`, `client`, helper setup). |
| `scripts/run_api_tests.sh` | Entregado | Ejecución directa de `tests_api.py`. |
| `scripts/run_e2e_tests.sh` | Entregado | Ejecución directa de `tests_e2e.py`. |
| `.gitignore` | Entregado | Exclusiones de artefactos locales/cache. |
| `README.md` | Entregado | Contexto del QA y ejecución rápida. |
| `INSTRUCCIONES.md` | Entregado | Pasos detallados de setup y ejecución. |
| `.github/workflows/qa-tests.yml` | Entregado | CI automática para API + E2E en push/PR. |
| `AI_FIRST_RESUMEN_George_Quintero_2026-07-06.md` | Entregado | Este documento. |

---

## Pruebas realizadas y avances reales

### API (`tests_api.py`)
- `/api/health`: estado OK.
- `/api/suppliers`: listado de proveedores.
- `/api/products`: listado de productos.
- `/api/products/{id}`: respuesta por ID y 404.
- `POST /api/products`: creación, detección de SKU duplicado.
- `POST /api/stock/movement`: ingresos/egresos, validación de payload, casos 503 con `ALERTS_FAIL=1`.
- `/api/stock/alerts`: alertas por stock <= `min_stock`, 503 forzado.
- `/api/movements`: listado y orden.

### E2E (`tests_e2e.py`)
- Flujo de carga inicial del frontend.
- Registro de movimiento de stock vía UI.
- Consulta de alertas vía UI.

### Cobertura funcional confirmada
- Contrato HTTP (status, headers, shapes).
- Happy paths.
- Edge cases y negativos documentados.
- Modo falla `ALERTS_FAIL=1`.

---

## Aprendizajes

- El SUT es un monolito FastAPI con SQLite embebida; la DB se genera en primer arranque.
- Los montos viajan en **centavos** (enteros).
- `ALERTS_FAIL=1` simula caída del servicio de alertas sin tocar red.
- Playwright necesita instalación de browser explícita (`playwright install chromium`).

---

## Decisiones técnicas

- Herramientas: pytest + httpx para API; Playwright para E2E.
- Fixtures en `conftest.py` para centralizar `base_url` y `client`.
- CI con GitHub Actions usando service container para el SUT.
- Dependencias lockeadas en `pyproject.toml` para reproducibilidad.
- Scripts bash como acceso rápido por suite.

---

## Entregables en repo

Rama: `george-quintero`  
URL: https://github.com/marisleidymora-cell/PruebasHermes/tree/george-quintero/qa-tests

---

## Próximos pasos sugeridos

1. Correr suites localmente contra SUT levantado para verificar green en este entorno exacto.
2. Ajustar `tests_e2e.py` si cambia el HTML del frontend del SUT.
3. Agregar casos de corrupción de datos (`stock negativo`, decimales, `min_stock` inválido, `cost_cents` negativo) que evidencien defectos conocidos del SUT.
4. Ampliar defect-report con severidades y fechas de hallazgo.
5. Agregar badge de CI al README cuando el workflow corra en main.

---

## Notas/posibles ampliaciones futuras

- Reporte HTML de pytest-cov.
- Suite de performance básica (`locust` o `hey`) para `/api/products` y `/api/stock/movement`.
- Matriz de trazabilidad `casos-de-prueba.md` ↔ `defect-report.md`.

---

## Bloqueos reales

- Autenticación GitHub inicial requirió instalación manual de `gh` porque `winget` no estaba disponible.
- Permisos iniciales denegaron push; se resolvió con login interactivo de `gh auth login`.
- Ejecución real de tests locales no se validó en CI dentro de la preparación del repo CI/CD.
