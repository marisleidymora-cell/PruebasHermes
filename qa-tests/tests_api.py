import os
import sys
from pathlib import Path

# Make SUT importable without copying app.py
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "3-challenge" / "gestor-inventario"))

import pytest
from fastapi.testclient import TestClient

from app import app, init_db

API_BASE = "http://testserver"


@pytest.fixture(autouse=True)
def database(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "inventario.db"))
    monkeypatch.delenv("ALERTS_FAIL", raising=False)
    init_db()
    yield


@pytest.fixture()
def api():
    with TestClient(app, base_url=API_BASE) as c:
        yield c


class TestContract:
    def test_health(self, api):
        r = api.get("/api/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

    def test_suppliers_fields(self, api):
        r = api.get("/api/suppliers")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list) and len(data) == 3
        required = ("id", "name", "email", "phone", "active")
        assert all(k in data[0] for k in required)
        assert isinstance(data[0]["active"], int)

    def test_products_fields(self, api):
        r = api.get("/api/products")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        if data:
            required = (
                "id", "name", "sku", "cost_cents", "price_cents",
                "stock", "min_stock", "supplier_id", "active"
            )
            assert all(k in data[0] for k in required)

    def test_product_detail_404(self, api):
        r = api.get("/api/products/999999")
        assert r.status_code == 404


class TestProductsCRUD:
    def test_create_returns_201_and_body(self, api):
        payload = {
            "name": "Cuaderno QA",
            "sku": "CUA-QA-UNIQUE-777",
            "cost_cents": 1200,
            "price_cents": 1800,
            "stock": 10,
            "min_stock": 2,
            "supplier_id": 1,
        }
        r = api.post("/api/products", json=payload)
        assert r.status_code == 201
        body = r.json()
        assert body["sku"] == payload["sku"]
        assert body["stock"] == payload["stock"]

    def test_duplicate_sku_returns_409(self, api):
        payload = {
            "name": "Cuaderno QA",
            "sku": "CUA-QA-502",
            "cost_cents": 1200,
            "price_cents": 1800,
            "stock": 10,
            "min_stock": 2,
            "supplier_id": 1,
        }
        api.post("/api/products", json=payload)
        r = api.post("/api/products", json=payload)
        assert r.status_code == 409
        assert "SKU" in r.json()["detail"]

    def test_invalid_supplier_returns_400(self, api):
        payload = {
            "name": "X", "sku": "X-1",
            "cost_cents": 1000, "price_cents": 2000,
            "stock": 0, "min_stock": 1, "supplier_id": 9999,
        }
        r = api.post("/api/products", json=payload)
        assert r.status_code == 400

    def test_missing_payload_returns_422(self, api):
        assert api.post("/api/products", json={"name": "X"}).status_code == 422


class TestStockMovements:
    def test_invalid_type_returns_400(self, api):
        assert api.post("/api/stock/movement", json={"product_id": 1, "type": "BAD", "qty": 1}).status_code == 400

    def test_missing_product_returns_404(self, api):
        assert api.post("/api/stock/movement", json={"product_id": 999, "type": "IN", "qty": 1}).status_code == 404

    def test_in_movement_updates_stock(self, api):
        before = api.get("/api/products/1").json()["stock"]
        r = api.post("/api/stock/movement", json={"product_id": 1, "type": "IN", "qty": 3})
        assert r.status_code == 201
        after = api.get("/api/products/1").json()["stock"]
        assert after == before + 3
        body = r.json()
        assert body["type"] == "IN" and body["qty"] == 3 and body["product_id"] == 1

    def test_out_movement_updates_stock(self, api):
        product_id = 6
        before = api.get(f"/api/products/{product_id}").json()["stock"]
        r = api.post("/api/stock/movement", json={"product_id": product_id, "type": "OUT", "qty": 2, "notes": "qa"})
        assert r.status_code == 201
        after = api.get(f"/api/products/{product_id}").json()["stock"]
        assert after == before - 2

    def test_movements_ordered_newest_first(self, api):
        for i in range(3):
            api.post("/api/stock/movement", json={"product_id": 1, "type": "IN", "qty": 1, "notes": str(i)})
        ids = [row["id"] for row in api.get("/api/movements").json()]
        assert ids == sorted(ids, reverse=True)

    def test_decimal_qty_is_accepted(self, api):
        r = api.post("/api/stock/movement", json={"product_id": 1, "type": "IN", "qty": 2.5})
        assert r.status_code == 201
        assert r.json()["qty"] == 2.5

    def test_negative_stock_after_out_movement(self, api):
        product_id = 1
        before = api.get(f"/api/products/{product_id}").json()["stock"]
        qty = before + 10
        r = api.post("/api/stock/movement", json={"product_id": product_id, "type": "OUT", "qty": qty})
        assert r.status_code == 201
        after = api.get(f"/api/products/{product_id}").json()["stock"]
        assert after == -(qty - before)


class TestIntegrationFailures:
    def test_alerts_503_when_failed(self, api):
        os.environ["ALERTS_FAIL"] = "1"
        try:
            assert api.get("/api/stock/alerts").status_code == 503
        finally:
            del os.environ["ALERTS_FAIL"]

    def test_out_movement_503_when_alerts_failed(self, api):
        os.environ["ALERTS_FAIL"] = "1"
        try:
            r = api.post("/api/stock/movement", json={"product_id": 1, "type": "OUT", "qty": 1})
            assert r.status_code == 503
        finally:
            del os.environ["ALERTS_FAIL"]

    def test_alerts_ok_when_healthy(self, api):
        r = api.get("/api/stock/alerts")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

