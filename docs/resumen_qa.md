# Resumen QA — Gestor de Inventario (rama `yeraldine`)
Qué hay: resumen del SUT, hallazgos, suites ejecutadas, comandos de corrida y reporte Allure.

## 1) ¿Qué es el SUT?

`gestor-inventario` es una aplicación FastAPI de archivo único (`app.py`) con frontend estático (`static/index.html`) y base de datos SQLite (`inventario.db`). Expone endpoints REST para:

- Proveedores (`/api/suppliers`)
- Productos (`/api/products`, `/api/products/{id}`)
- Movimientos de stock (`/api/stock/movement`) — tipo `IN`/`OUT`
- Alertas de stock mínimo (`/api/stock/alerts`)
- Historial de movimientos (`/api/movements`)

Incluye simulación de fallo del servicio de alertas con la variable de entorno `ALERTS_FAIL=1`.

> No se modificó el código del SUT. El trabajo es 100% pruebas y documentación.

---

## 2) Qué se hizo

Se diseñó y ejecutó una estrategia de pruebas completa sobre el SUT, aligned al reto QA:

- Pruebas de contrato y negocio por endpoint.
- Pruebas de integridad de datos.
- Pruebas de fallo simulado (`ALERTS_FAIL=1` → 503).
- Pruebas E2E con Playwright contra UI.

### 2.1 Pruebas API (httpx + pytest)

- `tests/api/test_api_contract.py`
- `tests/api/test_movements_log.py`
- `tests/api/test_stock_movements.py` (incluye 503 real vía servidor auxiliar y frontera de qty)
- `tests/api/test_negative_movements.py`
- `tests/api/test_data_integrity.py`
- `tests/api/test_frontend_smoke.py` (reclasificado desde E2E — ver nota abajo)

### 2.2 Pruebas E2E (Playwright, navegador real)

- `tests/e2e/test_playwright_suite.py`
- `tests/e2e/test_ui_registration_and_alerts.py` (incluye escenario 503 aislado)

**Total:** 28 pruebas (21 API + 5 E2E + 2 smoke de frontend).

> Nota de reclasificación: `tests/e2e/test_home.py` y `tests/e2e/test_frontend_flow.py` usaban `httpx`
> (sin navegador), así que no eran E2E de verdad. Se movieron a `tests/api/test_frontend_smoke.py` para
> que el conteo de "E2E" refleje solo pruebas que abren Chromium real.

---

## 3) Hallazgos

| ID | Severidad | Hallazgo |
|----|-----------|----------|
| D-01 | Alta | `POST /api/stock/movement` con `type=OUT` y cantidad mayor al stock disponible → acepta; stock queda negativo. |
| D-02 | Media | `qty` acepta valores decimales (`float`) cuando debería ser entero. |
| D-03 | Media | `POST /api/products` acepta `min_stock=-1` y `cost_cents=-1000` sin validación. |
| D-04 | Hallazgo de entorno | El 503 en `/api/stock/alerts` requiere que el SUT arranque con `ALERTS_FAIL=1` desde el inicio; no se reproduce activando la variable en caliente. Confirmado con servidor auxiliar tanto en API como en E2E. |
| D-05 | Media | `qty` negativo en un movimiento `IN` invierte la dirección: resta stock en vez de sumarlo. |
| D-06 | Baja | `qty=0` se acepta y queda en el historial de movimientos aunque no cambia el stock. |

---

## 4) Estado actual

- Suite completa: **28 passed, 0 failed** (21 API + 5 E2E + 2 smoke de frontend).
- Suite verificada repetible: corrida 3 veces seguidas sin cambios de resultado, gracias a la
  fixture `fresh_product` que aísla los datos de cada test.
- Rama: `yeraldine`.
- Documentación actualizada en `docs/` del repo QA.

---

## 5) Cómo correr todos los tests

### 5.1 Levantar el SUT (modo normal)

```bash
cd ~/Desktop/reto-ai-first-fase1/reto-ai-first-fase1/3-challenge/gestor-inventario
uvicorn app:app --port 8000
```

Verificar:

```bash
curl -s http://localhost:8000/api/health
```

### 5.2 Ejecutar la suite completa

```bash
cd ~/Desktop/PruebasHermes-trackQA
export BASE_URL=http://localhost:8000
export ALERTS_FAIL=0

python -m pytest -q
```

### 5.3 Ejecutar solo API

```bash
cd ~/Desktop/PruebasHermes-trackQA
export BASE_URL=http://localhost:8000
export ALERTS_FAIL=0

python -m pytest tests/api -q
```

### 5.4 Ejecutar solo E2E

```bash
cd ~/Desktop/PruebasHermes-trackQA
export BASE_URL=http://localhost:8000
export ALERTS_FAIL=0

python -m pytest tests/e2e -q
```

### 5.5 Ejecutar la prueba del escenario 503 (modo caída)

```bash
cd ~/Desktop/PruebasHermes-trackQA
BASE_URL=http://localhost:8000 ALERTS_FAIL=0 python -m pytest tests/e2e/test_ui_registration_and_alerts.py::test_alerts_section_shows_503_when_alert_service_down -q
BASE_URL=http://localhost:8000 ALERTS_FAIL=0 python -m pytest tests/api/test_stock_movements.py -k alerts_fail -q
```

> Nota: esas pruebas levantan automáticamente un servidor auxiliar con `ALERTS_FAIL=1` (helper
> centralizado en `tests/conftest.py`: `start_alerts_fail_server` / `stop_alerts_fail_server`),
> cada una en un puerto distinto para poder correr varias en paralelo sin pisarse.

## 5.6 Abrir el reporte Allure
```bash
allure serve ~/Desktop/PruebasHermes-trackQA/allure-results
```

## 5.7 Generar reporte Allure estático
```bash
allure generate --clean -o ~/Desktop/PruebasHermes-trackQA/allure-report ~/Desktop/PruebasHermes-trackQA/allure-results
open ~/Desktop/PruebasHermes-trackQA/allure-report/index.html
```

> Nota: `allure-results/` y `allure-report/` están ignorados en `.gitignore` para no subir artefactos.
