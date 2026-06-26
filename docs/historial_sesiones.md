# Bitácora QA — rama yeraldine
Última actualización: 2026-06-26

## Resumen del día
Hoy trabajamos en puro QA sobre el sistema `gestor-inventario`. No tocamos el código del sistema; solo armamos pruebas automáticas y documentación.

## Cambios que hicimos
- Documentación:
  - Actualizamos `docs/test_cases.md` con escenarios Gherkin.
  - Guardamos la ejecución real en `docs/ejecucion_suite_qa.md`.
  - Creamos esta bitácora para ir anotando lo que avanzamos.
- Pruebas automáticas:
  - API: agregamos `tests/api/test_negative_movements.py` y `tests/api/test_data_integrity.py`.
  - E2E: agregamos `tests/e2e/test_ui_registration_and_alerts.py`.
- Mantuvimos las pruebas anteriores que ya funcionaban:
  - `tests/api/test_api_contract.py`
  - `tests/api/test_movements_log.py`
  - `tests/api/test_stock_movements.py`
  - `tests/e2e/test_playwright_suite.py`
  - `tests/e2e/test_frontend_flow.py`

## Estado actual
- API: confirmada verde en `tests/api` (14 pruebas pasadas).
- E2E: confirmada verde en `tests/e2e/test_playwright_suite.py` con Chromium en modo headed.
- Servidor SUT: lo podemos levantar en `http://localhost:8000` cuando queramos correr las pruebas.

## Pendientes para mañana
- Correr una vez más `python -m pytest tests/api -q` y anotar el resultado aquí.
- Correr `python -m pytest tests/e2e -q` en modo headed y guardar la evidencia.
- Revisar si `docs/test_cases.md` coincide 1 a 1 con las pruebas que tenemos en código.
- Cerrar el faltante de 503 con `ALERTS_FAIL=1` si el entorno lo permite.
- Si aparece algún fallo nuevo, lo anotamos acá y lo corregimos sin tocar el código del SUT.

## Notas
- No se modificó el sistema `gestor-inventario` en ningún momento.
- Todo el trabajo quedó en la rama `yeraldine` del repo `PruebasHermes`.
- Mañana podés pedirme que lea este archivo y continuo sin volver a explicar todo.
