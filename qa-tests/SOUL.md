# SOUL.md — Reto AI-First · Track QA · gestor-inventario

## Proyecto
App bajo prueba: `3-challenge/gestor-inventario` del repo https://github.com/diegotrujillo-jikko/reto-ai-first-fase1.
Objetivo: ejecutar una estrategia de pruebas completa sin modificar el SUT.

## Cobertura
- Contrato API (status codes, campos, shapes de error).
- Funcional happy path + edge + negativos por endpoint.
- Integridad de datos tras movimientos IN/OUT.
- Fallo de integración `ALERTS_FAIL=1`.
- UI/E2E con Playwright sobre `http://localhost:8000`.

## Tooling
- pytest + FastAPI `TestClient` + httpx para API.
- Playwright para E2E.
- Ejecución real confirmada: `18 passed`.

## Decisiones
- Aislar `DB_PATH` por test y usar fixtures de API para evitar estado compartido.
- Usar SKUs únicos en pruebas de productos para evitar colisiones con seed.
- Reproducir bugs documentados del SUT con assertions positivas para acreditarlos.

## Hallazgos
- Stock negativo permitido.
- `qty` decimal aceptada.
- `min_status` negativo sin约束.
- `cost_cents` negativo sin约束.
- `ALERTS_FAIL=1` produce 503 en `/api/stock/alerts` y OUT movements.

## Bloqueos
- Python activo sin pip/uv accesible; resuelto creando venv con `uv` en `qa-tests/.venv`.
- Ejecutable `pytest` no hallado al inicio; resuelto con `.venv\Scripts\py.test.exe`.

## Repo
Workspace local: `C:\Users\DELL\reto-ai-first-fase1\qa-tests`
