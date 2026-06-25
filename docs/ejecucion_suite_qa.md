# Ejecución de la suite QA — rama yeraldine

## Contexto
- SUT: `gestor-inventario` en `/Users/admin/Desktop/reto-ai-first-fase1/reto-ai-first-fase1/3-challenge/gestor-inventario`
- Servidor levantado en `http://localhost:8000` con `uvicorn app:app`
- Ejecución de la suite desde `/Users/admin/Desktop/PruebasHermes-trackQA`

## Pasos realizados
1) Levantar el SUT en background con `uvicorn app:app --host 0.0.0.0 --port 8000`
2) Ejecutar `pytest tests/api -q`
3) Ajustar los tests según el comportamiento real observado
4) Generar documentación de entregable

## Comportamiento observado del SUT (modo normal)
- Health: `GET /api/health` → 200 + `{"status":"ok"}`
- Proveedores: `GET /api/suppliers` → lista con al menos 3 registros
- Productos: `GET /api/products` → lista con al menos 6 registros
- Producto inexistente: `GET /api/products/999999` → 404
- SKU duplicado: `POST /api/products` → 409
- Movimiento válido: `POST /api/stock/movement` → 201
- Movimiento con tipo inválido: 400
- Producto inexistente en movimiento: 404
- Movimiento OUT excede stock: **permite stock negativo**
- Movimiento con qty decimal: **acepta 1.5**
- `ALERTS_FAIL=1` en este ejecutable no disparó 503 en `/api/stock/alerts` ni en `POST ... OUT`

## Ajustes aplicados en la suite
- `tests/api/test_api_contract.py`: suite de contrato API (health, suppliers, products)
- `tests/api/test_movements_log.py`: validación de ordenamiento descendente
- `tests/api/test_stock_movements.py`: casos funcionales y de datos + alertas (modo limpio)
- `tests/conftest.py`: fixtures `client` y `BASE_URL` reutilizables
- `docs/plan.md`: plan de pruebas
- `docs/test_cases.md`: matriz de casos
- `docs/defect_report.md`: defectos detectados con severidad
- `SOUL.md`: proceso, herramientas, hallazgos

## Pendiente
- Documentar formalmente en este archivo la versión final de los tests que se commitearon
- Agregar acá la salida real de `pytest` una vez ejecutada la suite final
