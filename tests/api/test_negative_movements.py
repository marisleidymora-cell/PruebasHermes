"""
Suite de casos negativos para movimientos de stock.

Usa `fresh_product` (producto propio del test) cuando el caso necesita
un producto real, para no depender de los IDs semilla del SUT.
"""
import pytest


class TestNegativeMovements:
    def test_invalid_type_returns_400(self, client, fresh_product):
        r = client.post("/api/stock/movement", json={
            "product_id": fresh_product["id"],
            "type": "INVALID",
            "qty": 1,
            "notes": "",
        })
        assert r.status_code == 400

    def test_missing_product_returns_404(self, client):
        r = client.post("/api/stock/movement", json={
            "product_id": 999999,
            "type": "IN",
            "qty": 1,
            "notes": "",
        })
        assert r.status_code == 404
