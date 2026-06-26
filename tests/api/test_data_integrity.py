import pytest


class TestMovementDataIntegrity:
    def test_in_increases_stock_by_exact_qty(self, client):
        r = client.get("/api/products/1")
        assert r.status_code == 200
        before = r.json()["stock"]

        r = client.post("/api/stock/movement", json={
            "product_id": 1,
            "type": "IN",
            "qty": 7,
            "notes": "QA",
        })
        assert r.status_code == 201

        r = client.get("/api/products/1")
        assert r.json()["stock"] == before + 7

    def test_out_decreases_stock_by_exact_qty(self, client):
        r = client.get("/api/products/2")
        assert r.status_code == 200
        before = r.json()["stock"]

        r = client.post("/api/stock/movement", json={
            "product_id": 2,
            "type": "OUT",
            "qty": 3,
            "notes": "QA",
        })
        assert r.status_code == 201

        r = client.get("/api/products/2")
        assert r.json()["stock"] == before - 3
