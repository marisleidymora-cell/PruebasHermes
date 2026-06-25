# SOUL.md - PruebasHermes (Track QA)

## Proyecto probado
- SUT: `gestor-inventario` (FastAPI + SQLite + frontend estático)
- Repo base: `reto-ai-first-fase1/3-challenge/gestor-inventario`

## Estrategia
- API contract + funcional + integridad
- Ambiente: servidor local en `http://localhost:8000`
- Ejecución: `pytest` con `httpx` contra el SUT
- Modo ejecutado: SIN `ALERTS_FAIL=1` (ruta feliz)

## Herramientas
- Python 3.12
- pytest 9.1.1 + httpx 0.28.1
- uvicorn para levantar el SUT
- curl para diagnosis rápida

## Hallazgos observados (con evidencia)
- `POST /api/stock/movement` acepta `qty` decimal (`1.5`) → registra movimiento.
- `POST /api/stock/movement` con `type=OUT` y `qty > stock` → genera stock negativo.
- `POST /api/products` acepta `min_stock=-1` y `cost_cents=-1000` sin error.

## Uso de Hermes
- Generación y limpieza inicial de la rama `yeraldine`
- Generación de casos de prueba y documentación (plan, defect report)

## Issues / Bloqueos
- Acceso a GitHub: resuelto con `gh auth login`
- Pendiente: validar comportamiento con `ALERTS_FAIL=1` en un entorno controlado
