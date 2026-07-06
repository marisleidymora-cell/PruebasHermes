import os
import sys
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

APP_DIR = Path("/tmp/reto-ai-first-fase1/3-challenge/gestor-inventario")
sys.path.insert(0, str(APP_DIR))


class _EnvClient:
    """Create an isolated TestClient per test with its own DB file."""
    def __init__(self, tmpdb: Path):
        os.environ["DB_PATH"] = str(tmpdb)
        os.environ["ALERTS_FAIL"] = "0"
        # import after env is set so module globals pick up the right values
        from app import app, init_db
        self._app = app
        init_db()
        self.client = TestClient(app)


@pytest.fixture
def tc(tmp_path: Path):
    db = tmp_path / "test.db"
    client_wrap = _EnvClient(db)
    yield client_wrap.client


def test_health(tc):
    r = tc.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_suppliers_seeded(tc):
    r = tc.get("/api/suppliers")
    assert r.status_code == 200
    assert len(r.json()) == 3


def test_products_seeded(tc):
    r = tc.get("/api/products")
    assert r.status_code == 200
    assert len(r.json()) == 6
    assert {p["sku"] for p in r.json()} == {"PAP-001", "TON-002", "SIL-003", "MON-004", "TEC-005", "MOU-006"}


def test_create_product_conflict(tc):
    payload = {
        "name": "X",
        "sku": "PAP-001",
        "cost_cents": 100,
        "price_cents": 200,
        "stock": 1,
        "min_stock": 1,
        "supplier_id": 1,
    }
    r = tc.post("/api/products", json=payload)
    assert r.status_code == 409


def test_create_product_invalid_supplier(tc):
    payload = {
        "name": "Y",
        "sku": "NEW-002",
        "cost_cents": 1000,
        "price_cents": 2000,
        "stock": 1,
        "min_stock": 1,
        "supplier_id": 999,
    }
    r = tc.post("/api/products", json=payload)
    assert r.status_code == 400


def test_movement_bad_type(tc):
    r = tc.post("/api/stock/movement", json={"product_id": 1, "type": "BAD", "qty": 1})
    assert r.status_code == 400


def test_movement_unknown_product(tc):
    r = tc.post("/api/stock/movement", json={"product_id": 999, "type": "IN", "qty": 1})
    assert r.status_code == 404


def test_movement_in_updates_stock(tc):
    before = tc.get("/api/products/1").json()
    assert before["stock"] == 50
    r = tc.post("/api/stock/movement", json={"product_id": 1, "type": "IN", "qty": 10})
    assert r.status_code == 201
    after = tc.get("/api/products/1").json()
    assert after["stock"] == 60


def test_movement_out_decreases_stock(tc):
    before = tc.get("/api/products/2").json()
    assert before["stock"] == 12
    r = tc.post("/api/stock/movement", json={"product_id": 2, "type": "OUT", "qty": 3})
    assert r.status_code == 201
    after = tc.get("/api/products/2").json()
    assert after["stock"] == 9


def test_movement_out_allows_negative_stock(tc):
    r = tc.post("/api/stock/movement", json={"product_id": 2, "type": "OUT", "qty": 999})
    assert r.status_code == 201
    p = tc.get("/api/products/2").json()
    assert p["stock"] < 0


def test_stock_alerts_normal(tc):
    j = {
        "name": "AlertaPrueba",
        "sku": "ALT-001",
        "cost_cents": 1000,
        "price_cents": 2000,
        "stock": 1,
        "min_stock": 2,
        "supplier_id": 1,
    }
    assert tc.post("/api/products", json=j).status_code == 201
    r = tc.get("/api/stock/alerts")
    assert r.status_code == 200
    data = r.json()
    assert any(x["sku"] == "ALT-001" for x in data)


def test_alerts_simulated_failure(tc):
    os.environ["ALERTS_FAIL"] = "1"
    try:
        r = tc.get("/api/stock/alerts")
        assert r.status_code == 503
    finally:
        os.environ["ALERTS_FAIL"] = "0"


def test_out_movement_alerts_failure_propagates(tc):
    os.environ["ALERTS_FAIL"] = "1"
    try:
        r = tc.post("/api/stock/movement", json={"product_id": 1, "type": "OUT", "qty": 1})
        assert r.status_code == 503
    finally:
        os.environ["ALERTS_FAIL"] = "0"


def test_movements_history(tc):
    tc.post("/api/stock/movement", json={"product_id": 1, "type": "IN", "qty": 5})
    r = tc.get("/api/movements")
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) >= 1
    assert rows[0]["type"] == "IN"
    assert rows[0]["product_id"] == 1


def test_get_product_by_id_not_found(tc):
    r = tc.get("/api/products/999")
    assert r.status_code == 404


def test_create_product_success(tc):
    payload = {
        "name": "Nuevo",
        "sku": "NEW-001",
        "cost_cents": 1000,
        "price_cents": 2000,
        "stock": 10,
        "min_stock": 2,
        "supplier_id": 1,
    }
    r = tc.post("/api/products", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["sku"] == "NEW-001"
    assert data["stock"] == 10


def test_out_movement_record_qty(tc):
    r = tc.post("/api/stock/movement", json={"product_id": 1, "type": "OUT", "qty": 1, "notes": "sale"})
    assert r.status_code == 201
    body = r.json()
    assert body["type"] == "OUT"
    assert body["qty"] == 1
