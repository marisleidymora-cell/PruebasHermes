# INSTRUCCIONES - QA-TRACK

## 0. Requisitos

- Python 3.10+
- `uv` (gestor de paquetes)
- `gh` CLI (para manejo del repo)

## 1. Clonar el repositorio

```bash
git clone -b george-quintero https://github.com/marisleidymora-cell/PruebasHermes.git
cd PruebasHermes
```

## 2. Crear entorno virtual

```bash
cd qa-tests
uv venv
```

Windows PowerShell:
```powershell
cd qa-tests
uv venv
```

## 3. Instalar dependencias

```bash
uv pip install pytest httpx playwright
playwright install chromium
```

## 4. Levantar el SUT (System Under Test)

El SUT está en: `3-challenge/gestor-inventario/`

Opción A — Docker:
```bash
cd 3-challenge/gestor-inventario
docker compose up --build
```

Opción B — Local:
```bash
cd 3-challenge/gestor-inventario
uvicorn app:app --port 8000
```

Simular fallo de alertas:
```bash
cd 3-challenge/gestor-inventario
ALERTS_FAIL=1 uvicorn app:app --port 8000
```

Ver docs: http://localhost:8000/docs

## 5. Ejecutar las pruebas API

 Desde `qa-tests/`:
```bash
uv run pytest tests_api.py -v
```

## 6. Ejecutar las pruebas E2E

```bash
uv run pytest tests_e2e.py -v
```

## 7. Ejecutar todas las pruebas

```bash
uv run pytest -v
```

## 8. Estructura del proyecto

```
qa-tests/
├── .gitignore
├── README.md              ← este archivo
├── SOUL.md                ← bitácora de proceso
├── plan-de-pruebas.md     ← plan de testing
├── casos-de-prueba.md     ← casos documentados
├── defect-report.md       ← hallazgos
├── tests_api.py           ← suite API
└── tests_e2e.py           ← suite E2E
```

## Notas

- Todos los montos en la API son en **centavos** (enteros)
- `ALERTS_FAIL=1` fuerza 503 en `/api/stock/alerts` y `POST /api/stock/movement` (type=OUT)
- No modificar el SUT, solo testear
