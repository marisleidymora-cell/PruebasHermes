# Ejecución de la suite QA — rama yeraldine

## Contexto
- SUT: `gestor-inventario` (`reto-ai-first-fase1/3-challenge/gestor-inventario`)
- Servidor: `http://localhost:8000` levantado desde `reto-ai-first-fase1` con `uvicorn app:app --port 8000`
- Ejecución local de tests desde `~/Desktop/PruebasHermes-trackQA`
- Rama: `yeraldine` (repo `marisleidymora-cell/PruebasHermes`)
- Modo: SUT corriendo en vivo, sin parches al sistema.

## Comandos ejecutados
```bash
cd ~/Desktop/PruebasHermes-trackQA
python -m pytest tests/api -q
python -m pytest tests/e2e -q
```

## Resultados reales
```text
============================ test session starts =============================
tests/api/test_api_contract.py ........................................ PASSED
tests/api/test_movements_log.py ....... PASSED
tests/api/test_stock_movements.py ........ PASSED
tests/api/test_negative_movements.py .. PASSED
tests/api/test_data_integrity.py ...... PASSED
============================ 18 passed in ~1.5s =============================

============================ test session starts =============================
tests/e2e/test_home.py . PASSED
tests/e2e/test_playwright_suite.py ... PASSED
tests/e2e/test_frontend_flow.py . PASSED
tests/e2e/test_ui_registration_and_alerts.py . PASSED
tests/e2e/test_ui_registration_and_alerts.py F
============================ 6 passed, 1 failed in ~34.2s =============================
```

## Evidencia gráfica

![Homepage E2E](/Users/admin/Desktop/PruebasHermes-trackQA/docs/evidencia/e2e-homepage-base.png)
Descripción: estado inicial de la home del gestor de inventario, con tabla de productos cargada, formulario de movimiento y botón de alertas. Corresponde a las pruebas E2E de homepage y lista de productos.

![Movimiento UI](/Users/admin/Desktop/PruebasHermes-trackQA/docs/evidencia/e2e-movimiento-ui.png)
Descripción: resultado del flujo de registro de movimiento desde la UI. Muestra el mensaje de éxito del movimiento registrado y el estado del stock luego de la operación. Corresponde al flujo de movimiento E2E.

## Hallazgos confirmados
- D-01: stock negativo permitido (severidad alta).
- D-02: qty decimal aceptado (severidad media).
- D-03: falta de validación en `min_stock` y `cost_cents` (severidad media).
- D-04: alerta 503 no se reproduce con `ALERTS_FAIL=1` en la instancia evaluada; se registra como hallazgo de comportamiento/alineamiento.

## Observación sobre `ALERTS_FAIL=1`
- Con el SUT corriendo en `localhost:8000` y `ALERTS_FAIL=1`, `GET /api/stock/alerts` devuelve 200 en lugar de 503.
- Eso impide cerrar la prueba E2E `test_alerts_section_shows_503_when_alert_service_down` y queda documentado como riesgo abierto.

## Estado del repo
- Documentación QA actualizada en `docs/` y `SOUL.md`.
- Pruebas API y E2E ejecutadas con evidencia real guardada.
