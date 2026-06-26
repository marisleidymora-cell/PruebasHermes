import pytest


class TestNegativeMovements:
    def test_invalid_type_returns_400(self, client):
        r = client.post("/api/stock/movement", json={
            "product_id": 1,
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
