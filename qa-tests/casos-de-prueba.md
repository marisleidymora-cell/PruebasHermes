# Casos de Prueba — gestor-inventario

## Contract / API
- TC-01 Health `GET /api/health` → 200 `{"status":"ok"}`
- TC-02 Suppliers `GET /api/suppliers` → 200, lista de 3, campos completos, active int
- TC-03 Products `GET /api/products` → 200, campos requeridos
- TC-04 Product detail `GET /api/products/999999` → 404
- TC-05 Create product 201 y duplicate SKU 409

## Funcional movimientos
- TC-06 Tipo inválido → 400
- TC-07 Producto inexistente movimiento → 404
- TC-08 IN incrementa stock exactamente
- TC-09 OUT descuenta stock correctamente
- TC-10 Movimientos ordenados descendente

## Negativos/bugs SUT
- TC-11 Movimiento OUT mayor a stock → 201 y stock negativo
- TC-12 qty decimal 2.5 aceptada → 201 y valor 2.5
- TC-13 `ALERTS_FAIL=1` alerts → 503
- TC-14 `ALERTS_FAIL=1` OUT movement → 503
- TC-15 alerts healthy → 200

## E2E
- TC-16 Home carga y frontend disponible en `/`
- TC-17 UI pública y responsive básica
