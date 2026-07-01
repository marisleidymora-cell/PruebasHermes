"""
Suite de integridad de datos para `gestor-inventario`.

Cobertura:
- Movimiento IN aumenta stock exactamente por la cantidad enviada.
- Movimiento OUT disminuye stock exactamente por la cantidad enviada.

Usa la fixture `fresh_product` (producto propio, creado por el test) en vez
de los productos semilla (id=1, id=2). Así cada corrida parte de un stock
conocido y no se acumulan cambios de corridas anteriores: la suite se puede
ejecutar N veces seguidas y siempre da el mismo resultado.
"""
import pytest


class TestMovementDataIntegrity:
    """Verifica que los movimientos modifiquen el stock de forma exacta."""

    def test_in_increases_stock_by_exact_qty(self, client, fresh_product):
        """
        happy path IN:
        - Partimos del stock inicial del producto propio del test (50).
        - Enviamos un movimiento IN de 7 unidades.
        - Validamos que el stock final sea inicial + 7.
        """
        before = fresh_product["stock"]

        r = client.post("/api/stock/movement", json={
            "product_id": fresh_product["id"],
            "type": "IN",                     # Entrada de stock.
            "qty": 7,
            "notes": "QA",
        })
        assert r.status_code == 201           # Movimiento registrado.

        r = client.get(f"/api/products/{fresh_product['id']}")     # Estado posterior.
        assert r.json()["stock"] == before + 7

    def test_out_decreases_stock_by_exact_qty(self, client, fresh_product):
        """
        happy path OUT:
        - Partimos del stock inicial del producto propio del test (50).
        - Enviamos un movimiento OUT de 3 unidades.
        - Validamos que el stock final sea inicial - 3.
        """
        before = fresh_product["stock"]

        r = client.post("/api/stock/movement", json={
            "product_id": fresh_product["id"],
            "type": "OUT",                    # Salida de stock.
            "qty": 3,
            "notes": "QA",
        })
        assert r.status_code == 201           # Movimiento registrado.

        r = client.get(f"/api/products/{fresh_product['id']}")     # Estado posterior.
        assert r.json()["stock"] == before - 3
