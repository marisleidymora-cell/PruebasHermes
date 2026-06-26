# Bitácora QA — rama yeraldine
Última actualización: 2026-06-26

## Resumen del día
Hoy trabajamos en puro QA sobre el sistema `gestor-inventario`. No tocamos el código del sistema; solo armamos pruebas automáticas y documentación.

## Cambios que hicimos
- Documentación:
  - Actualizamos `docs/test_cases.md` para alinear el escenario de alertas caídas.
  - Guardamos la ejecución real en `docs/ejecucion_suite_qa.md`.
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

## Estado actual
- API: confirmada verde en `tests/api` (18 pruebas pasadas).
- E2E: suite completa ejecutada (`tests/e2e -q`) con SUT levantado en `http://localhost:8000`.
  - 6 pruebas pasadas.
  - 1 prueba fallida: `test_alerts_section_shows_503_when_alert_service_down` por timeout esperando `/api/stock/alerts`.
    - Causa confirmada: con SUT corriendo, `ALERTS_FAIL=1` no dispara 503 en `/api/stock/alerts`; no es bloqueo de red.
    - Clasificación: hallazgo de comportamiento / limitación del escenario simulado.

## Pendientes / Riesgos abiertos
- Escenario 503 desde UI (E2E): no cerrado porque el comportamiento del SUT no replica el fallo simulado documentado en la guía del reto.

## Notas
- No se modificó el sistema `gestor-inventario` en ningún momento.
- Todo el trabajo quedó en la rama `yeraldine` del repo `PruebasHermes`.
- Podés pedirme que lea cualquiera de los docs para continuar sin repetir contexto.
