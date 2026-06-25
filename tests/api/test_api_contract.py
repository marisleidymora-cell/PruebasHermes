import uuid
import pytest


class TestHealth:
    def test_health_returns_200(self, client):
        r = client.get("/api/health")
        assert r.status_code == 200
        body = r.json()
        assert isinstance(body, dict)
        assert body.get("status") == "ok"


class TestSuppliers:
    def test_list_suppliers_returns_array(self, client):
        r = client.get("/api/suppliers")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) >= 1


class TestProducts:
    def test_list_products_returns_array(self, client):
        r = client.get("/api/products")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_existing_product_fields(self, client):
        r = client.get("/api/products/1")
        assert r.status_code == 200
        p = r.json()
        for k in ("id", "name", "sku", "cost_cents", "price_cents", "stock", "min_stock", "supplier_id"):
            assert k in p

    def test_get_missing_product_returns_404(self, client):
        r = client.get("/api/products/999999")
        assert r.status_code == 404

    def test_create_product_201(self, client):
        payload = {
            "name": "Libreta A4",
            "sku": f"SKU-{uuid.uuid4().hex[:8]}",
            "cost_cents": 1500,
            "price_cents": 2500,
            "stock": 100,
            "min_stock": 10,
            "supplier_id": 1,
        }
        r = client.post("/api/products", json=payload)
        assert r.status_code == 201
        p = r.json()
        assert p["sku"] == payload["sku"]
        assert p["stock"] == 100

    def test_create_product_duplicate_sku_409(self, client):
        payload = {
            "name": "SKU duplicado",
            "sku": "PAP-001",
            "cost_cents": 1000,
            "price_cents": 2000,
            "stock": 5,
            "min_stock": 2,
            "supplier_id": 1,
        }
        r = client.post("/api/products", json=payload)
        assert r.status_code == 409

    def test_create_product_allows_negative_min_stock(self, client):
        payload = {
            "name": "Min stock negativo",
            "sku": f"SKU-{uuid.uuid4().hex[:8]}",
            "cost_cents": 1000,
            "price_cents": 2000,
            "stock": 10,
            "min_stock": -1,
            "supplier_id": 1,
        }
        r = client.post("/api/products", json=payload)
        assert r.status_code == 201

    def test_create_product_allows_negative_cost(self, client):
        payload = {
            "name": "Costo negativo",
            "sku": f"SKU-{uuid.uuid4().hex[:8]}",
            "cost_cents": -1000,
            "price_cents": 1000,
            "stock": 0,
            "min_stock": 1,
            "supplier_id": 1,
        }
        r = client.post("/api/products", json=payload)
        assert r.status_code == 201


class TestMovements:
    def test_list_movements_returns_array(self, client):
        r = client.get("/api/movements")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
