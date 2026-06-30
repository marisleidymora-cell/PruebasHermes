# Bitácora QA — rama yeraldine
Última actualización: 2026-06-30

## Resumen del día
Hoy trabajamos en puro QA sobre el sistema `gestor-inventario`. No tocamos el código del sistema; solo armamos pruebas automáticas y documentación.

## Cambios que hicimos
- Documentación:
  - Actualizamos `docs/test_cases.md` para alinear el escenario de alertas caídas.
  - Guardamos la ejecución real en `docs/ejecucion_suite_qa.md` con capturas de evidencia.
  - Creamos esta bitácora para ir anotando lo que avanzamos.
- Pruebas API:
  - `tests/api/test_api_contract.py`
  - `tests/api/test_movements_log.py`
  - `tests/api/test_stock_movements.py`
  - `tests/api/test_negative_movements.py`
  - `tests/api/test_data_integrity.py`
- Pruebas E2E:
  - `tests/e2e/test_playwright_suite.py`
  - `tests/e2e/test_frontend_flow.py`
  - `tests/e2e/test_ui_registration_and_alerts.py`
  - `tests/e2e/test_home.py` ajustada para exponer fixture y URL base.
- Evidencia:
  - Capturas de E2E en `docs/evidencia/` insertadas en `docs/ejecucion_suite_qa.md`.
- Repo:
  - Commit y push en rama `yeraldine`.
  - Limpieza de `.DS_Store` en `.gitignore`.

## Estado actual
- API: confirmada verde en `tests/api` (18 pruebas pasadas).
- E2E: suite completa ejecutada (`tests/e2e -q`) con SUT levantado en `http://localhost:8000`.
  - 9 pruebas pasadas.
  - 0 pruebas fallidas.
- Cierre de pendiente: `test_alerts_section_shows_503_when_alert_service_down` ajustada para levantar un servidor auxiliar con `ALERTS_FAIL=1` y validar 503 desde la UI.
  - Clasificación: hallazgo cubierto con prueba automatizada.

## Pendientes / Riesgos abiertos
- Ninguno pendiente documentado.

## Notas
- No se modificó el sistema `gestor-inventario` en ningún momento.
- Todo el trabajo quedó en la rama `yeraldine` del repo `PruebasHermes`.
- Documentación adicional: `docs/resumen_qa.md` con descripción del SUT, hallazgos y comandos de ejecución.
