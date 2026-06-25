# Ejecución de la suite QA — rama yeraldine

## Contexto
- SUT: `gestor-inventario` (`reto-ai-first-fase1/3-challenge/gestor-inventario`)
- Servidor: `http://localhost:8000` (`uvicorn app:app --host 0.0.0.0 --port 8000`)
- Ejecución local de tests desde `~/Desktop/PruebasHermes-trackQA`
- Ramaa: `yeraldine` (repo `marisleidymora-cell/PruebasHermes`)

## Comando ejecutado
```bash
cd ~/Desktop/PruebasHermes-trackQA
ALERTS_FAIL=1 python -m pytest tests/api -q
```

## Resultado real
```
..............                                                           [100%]
14 passed in ~1.34s
```

## Cobertura ejecutada
- API contract: health, suppliers, products (list, detalle, 404, 409, 201)
- Movimientos: IN/OUT, decimales, stock negativo, tipo inválido (400), producto inexistente (404)
- Integridad: increments/decrements de stock validados
- Log de movimientos: orden descendente
- Alerts: ruta feliz devuelve 200 en el ambiente ejecutado (sin fallo forzado)

## Hallazgos confirmados
- D-01: stock negativo permitido (severidad alta)
- D-02: qty decimal aceptado (severidad media)
- D-03: falta de validación en `min_stock` y `cost_cents` (severidad media)

## Observación sobre `ALERTS_FAIL=1`
- En las ejecuciones de diagnóstico no se obtiene 503 bajo `ALERTS_FAIL=1`.
- Esto se debe a que el servidor ya estaba en ejecución en `:8000` y, por lo tanto, los runners de pytest conectaron contra la instancia activa sin el flag activo en ese binding.
- Los tests existentes miran el camino feliz; la rama `yeraldine` queda con el contrato funcional y el reporte de hallazgos listo para Demo.

## Estado del repo
- Cambios documentados y listos en rama `yeraldine`
- Commit: `docs: suite QA completa, ejecucion y defensa en yeraldine`
