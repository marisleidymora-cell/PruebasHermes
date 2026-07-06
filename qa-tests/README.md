# QA-TRACK · PruebasHermes

Artefactos del Track QA para el reto `reto-ai-first-fase1`. SUT: gestor-inventario(3-challenge/gestor-inventario).

## Entregables

- `SOUL.md` — bitácora de proceso, estrategia y decisiones
- `plan-de-pruebas.md` — alcance, criterios, niveles de prueba
- `casos-de-prueba.md` — casos happy/edge/negative
- `defect-report.md` — hallazgos, severidad, evidencia
- `tests_api.py` — suite API (pytest + httpx)
- `tests_e2e.py` — suite E2E frontend (Playwright)

## Ejecución rápida

```bash
cd 3-challenge/gestor-inventario
uvicorn app:app --port 8000

# terminal 2
cd qa-tests
uv run pytest tests_api.py -v
uv run pytest tests_e2e.py -v
```

> Variables: `ALERTS_FAIL=1` fuerza fallo del servicio de alertas para pruebas de 503.
