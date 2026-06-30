"""
Suite de integridad de datos para `gestor-inventario`.

Cobertura:
- Movimiento IN aumenta stock exactamente por la cantidad enviada.
- Movimiento OUT disminuye stock exactamente por la cantidad enviada.

Se consulta el estado previo y posterior del producto para asegurar
que no se pierda precisión en la actualización.
"""
import pytest


class TestMovementDataIntegrity:
    """Verifica que los movimientos modifiquen el stock de forma exacta."""

    def test_in_increases_stock_by_exact_qty(self, client):
        """
        happy path IN:
        - Consultamos stock inicial del producto 1.
        - Enviamos un movimiento IN de 7 unidades.
        - Validamos que el stock final sea inicial + 7.
        """
        r = client.get("/api/products/1")     # Estado base del producto.
        assert r.status_code == 200
        before = r.json()["stock"]

        r = client.post("/api/stock/movement", json={
            "product_id": 1,
            "type": "IN",                     # Entrada de stock.
            "qty": 7,
            "notes": "QA",
        })
        assert r.status_code == 201           # Movimiento registrado.

        r = client.get("/api/products/1")     # Estado posterior.
        assert r.json()["stock"] == before + 7

    def test_out_decreases_stock_by_exact_qty(self, client):
        """
        happy path OUT:
        - Consultamos stock inicial del producto 2.
        - Enviamos un movimiento OUT de 3 unidades.
        - Validamos que el stock final sea inicial - 3.

        Nota: si ALERTS_FAIL=1 está activo, este endpoint puede responder 503
        y la prueba pasa a ser smoke de fallo; en modo normal debe ser 201.
        """
        r = client.get("/api/products/2")     # Estado base del producto.
        assert r.status_code == 200
        before = r.json()["stock"]

        r = client.post("/api/stock/movement", json={
            "product_id": 2,
            "type": "OUT",                    # Salida de stock.
            "qty": 3,
            "notes": "QA",
        })
        assert r.status_code == 201           # Movimiento registrado.

        r = client.get("/api/products/2")     # Estado posterior.
        assert r.json()["stock"] == before - 3
