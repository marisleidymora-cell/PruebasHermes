# SOUL.md — Reto AI-First · Fase 1 · Track QA
## Log del proceso
- Repo clonado: `https://github.com/diegotrujillo-jikko/reto-ai-first-fase1`
- SUT inspeccionado: `3-challenge/gestor-inventario/app.py`
- Suite API generada: `gestor-inventario/tests/test_sut.py`
- Corrida local: 17/17 (verificación ad-hoc + pytest)
- Suite E2E: pendiente
- Reporte de defectos: pendiente

## Scope
- Alcance puro: API REST + frontend estático del Gestor de Inventario (FastAPI + SQLite).
- No está en scope modificar producción salvo para crear la suite E2E si se requiere.
- Se documentan hallazgos/residual risks sin alterar el SUT.

## Tooling
- Python 3.13
- fastapi, uvicorn[standard], httpx
- pytest
- Playwright (deseable/posible)

## Estrategia
- API first, backend-driven.
- Suite API: contrato + validaciones de error con `TestClient`.
- E2E: si se incluye, contra `localhost:8000` servido en background.
- Aislar estado por test con DB en memoria/archivo temporal.

## Hallazgos previos
- `qty` acepta decimales sin restricción.
- `OUT` no valida saldo suficiente; permite stock negativo.
- `/api/products` no expone `sku` en `/api/stock/alerts` según la inspección esperada.

## Blockers
- Sin bloqueo actual para ejecutar API suite.
- E2E requiere levantamiento estable del servicio en background.
- No hay PDFs/documentos de requerimientos parseables en Markdown en este repo; se usan PDFs en `3-challenge/`.
