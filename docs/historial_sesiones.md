# Bitácora QA — rama yeraldine
Última actualización: 2026-07-01 (sesión 2)
Qué hay: registro de cambios, estado actual y pendientes del trabajo QA.

## Resumen del día (sesión 2)
Se pidió una revisión detenida de la calidad de los tests existentes, no solo de la documentación.
Se encontraron 5 problemas reales en la suite y se corrigieron todos, con evidencia de que la suite
sigue en verde y ahora es repetible (antes no lo era).

## Problemas encontrados y cómo se corrigieron

1. **Assert que nunca podía fallar.**
   `test_alerts_with_failure_returns_503` aceptaba `status_code in (201, 503)` — no importaba qué
   devolviera el SUT, el test siempre pasaba. Se reemplazó por dos tests reales
   (`test_alerts_with_alerts_fail_returns_503` y `test_out_movement_with_alerts_fail_returns_503`)
   que corren contra un servidor auxiliar con `ALERTS_FAIL=1` de verdad activo, así que ahora sí
   pueden fallar si el comportamiento cambia.

2. **"E2E" que en realidad eran pruebas de API.**
   `tests/e2e/test_home.py` y `tests/e2e/test_frontend_flow.py` usaban `httpx` (peticiones HTTP
   directas), nunca abrían un navegador. Se movieron a `tests/api/test_frontend_smoke.py` y se les
   quitó la etiqueta E2E. Ahora el conteo de "pruebas E2E" refleja solo pruebas que abren Chromium.

3. **Test con nombre engañoso.**
   `test_alert_query_flow` decía probar el flujo de alertas pero solo abría la home y verificaba
   que no estuviera vacía — nunca tocaba el botón de alertas. Se reescribió para hacer click real
   en "Consultar alertas" y verificar la respuesta HTTP y el DOM.

4. **Datos no aislados entre tests (el hallazgo más importante).**
   Varios tests sumaban/restaban stock directo sobre los productos semilla (id=1, id=2) sin
   limpiar después. Si se corría la suite dos veces seguidas, el stock quedaba distinto cada vez.
   Se creó la fixture `fresh_product` en `conftest.py`, que crea un producto nuevo y único por
   test. Se aplicó en `test_stock_movements.py`, `test_data_integrity.py` y
   `test_negative_movements.py`. Se verificó corriendo la suite completa 3 veces seguidas: mismo
   resultado siempre (28 passed).

5. **Faltaban casos de frontera para `qty`.**
   Se agregaron 2 tests nuevos en `test_stock_movements.py::TestMovementQtyBoundaries`:
   - `qty=0`: se acepta (201) y no cambia el stock, pero sí queda en el historial (D-06).
   - `qty` negativo en un `IN`: se acepta (201) y resta stock en vez de sumar — invierte la
     dirección del movimiento sin avisar (D-05).

## Otros cambios de limpieza
- Se centralizó en `tests/conftest.py` la lógica para levantar el servidor auxiliar con
  `ALERTS_FAIL=1` (`start_alerts_fail_server` / `stop_alerts_fail_server`), que antes estaba
  duplicada en `tests/e2e/test_ui_registration_and_alerts.py` y en un archivo suelto
  `tests/e2e/_server.py` que nadie usaba. Se eliminó ese archivo duplicado.
- Se detectó y corrigió un problema de puertos: dos tests que usan servidor auxiliar podían
  chocar en el mismo puerto si un proceso anterior tardaba en cerrar. Ahora cada test recibe
  un puerto distinto y se espera a que el proceso termine antes de continuar.

## Estado actual
- Suite completa: **28 passed, 0 failed** (21 API + 5 E2E reales + 2 smoke de frontend).
- Verificado repetible: 3 corridas seguidas, mismo resultado cada vez.
- Ningún proceso auxiliar queda colgado después de correr la suite (verificado con `ps aux`).

## Pendientes / Riesgos abiertos
- Riesgo (no bloqueante): los tests del escenario 503 (API y E2E) dependen de la ruta local
  `~/Desktop/reto-ai-first-fase1/reto-ai-first-fase1/3-challenge/gestor-inventario` para levantar
  su servidor auxiliar. Si esa carpeta se mueve, esos tests dejan de poder aislar el escenario.

## Notas
- No se modificó el sistema `gestor-inventario` en ningún momento.
- Todo el trabajo quedó en la rama `yeraldine` del repo `PruebasHermes`.
- Documentación adicional: `docs/resumen_qa.md` con descripción del SUT, hallazgos y comandos de ejecución.

