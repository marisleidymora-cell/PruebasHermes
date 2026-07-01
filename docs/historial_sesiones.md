# Bitácora QA — rama yeraldine
Última actualización: 2026-07-01
Qué hay: registro de cambios, estado actual y pendientes del trabajo QA.

## Resumen del día
Hoy revisamos toda la documentación existente contra el código real de tests, corregimos desalineaciones
detectadas (conteo de pruebas, caso 503, defecto D-04, caso TC-API-18 sin documentar) y volvimos a correr
la suite completa contra el SUT en vivo para confirmar el estado real.

## Cambios que hicimos
- Documentación:
  - `docs/test_cases.md`: se agregó TC-API-18 (`tests/api/test_movements_log.py`, antes sin documentar) y
    se corrigió el estado de TC-E2E-05 (503) de "pendiente" a "resuelto".
  - `SOUL.md`: se actualizó el hallazgo 4 (ALERTS_FAIL) para reflejar que el escenario 503 SÍ está cubierto
    con un servidor auxiliar aislado, y se documentó el riesgo residual de ruta local fija.
  - `docs/defect_report.md`: se agregó D-04 (dependencia de arranque con ALERTS_FAIL=1) que ya se mencionaba
    en otros docs pero faltaba en el reporte de defectos.
  - Se unificó el conteo de pruebas a 25 (18 API + 7 E2E) en todos los documentos.

## Estado actual
- API: 18 pruebas verdes en `tests/api`.
- E2E: 7 pruebas verdes en `tests/e2e`.
- Total: 25 passed, 0 failed (verificado hoy con `python -m pytest -v` contra SUT real en `localhost:8000`).
- Caso 503: cubierto con servidor auxiliar aislado en el test E2E; riesgo residual documentado (ruta local fija).

## Pendientes / Riesgos abiertos
- Riesgo (no bloqueante): `test_alerts_section_shows_503_when_alert_service_down` depende de la ruta local
  `~/Desktop/reto-ai-first-fase1/reto-ai-first-fase1/3-challenge/gestor-inventario` para levantar su servidor
  auxiliar. Si esa carpeta se mueve, el test deja de poder aislar el escenario.

## Notas
- No se modificó el sistema `gestor-inventario` en ningún momento.
- Todo el trabajo quedó en la rama `yeraldine` del repo `PruebasHermes`.
- Documentación adicional: `docs/resumen_qa.md` con descripción del SUT, hallazgos y comandos de ejecución.

