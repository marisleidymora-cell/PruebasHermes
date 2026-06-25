import pytest


FIXED_PRODUCT_ID = 1


class TestStockMovements:
    def test_movement_in_201_and_increments_stock(self, client):
        p = client.get(f"/api/products/{FIXED_PRODUCT_ID}").json()
        initial_stock = p["stock"]

        payload = {"product_id": FIXED_PRODUCT_ID, "type": "IN", "qty": 5}
        r = client.post("/api/stock/movement", json=payload)
        assert r.status_code == 201
        m = r.json()
        assert m["type"] == "IN"
        assert m["qty"] == 5

        after = client.get(f"/api/products/{FIXED_PRODUCT_ID}").json()
        assert after["stock"] == initial_stock + 5

    def test_movement_out_201_and_decrements_stock(self, client):
        p = client.get(f"/api/products/{FIXED_PRODUCT_ID}").json()
        initial_stock = p["stock"]

        # Ensure we don't break future tests: add stock back
        if initial_stock == 0:
            client.post("/api/stock/movement", json={"product_id": FIXED_PRODUCT_ID, "type": "IN", "qty": 10})

        payload = {"product_id": FIXED_PRODUCT_ID, "type": "OUT", "qty": 2}
        r = client.post("/api/stock/movement", json=payload)
        assert r.status_code == 201
        m = r.json()
        assert m["type"] == "OUT"

        after = client.get(f"/api/products/{FIXED_PRODUCT_ID}").json()
        assert after["stock"] == initial_stock + 10 - 2

    def test_movement_out_negative_stock_allowed(self, client):
        payload = {"product_id": FIXED_PRODUCT_ID, "type": "OUT", "qty": 999999}
        r = client.post("/api/stock/movement", json=payload)
        assert r.status_code == 201

    def test_movement_decimal_qty_accepted(self, client):
        payload = {"product_id": FIXED_PRODUCT_ID, "type": "IN", "qty": 2.5}
        r = client.post("/api/stock/movement", json=payload)
        assert r.status_code == 201

    def test_movement_invalid_type_400(self, client):
        payload = {"product_id": FIXED_PRODUCT_ID, "type": "INVALID", "qty": 1}
        r = client.post("/api/stock/movement", json=payload)
        assert r.status_code == 400

    def test_movement_product_not_found_404(self, client):
        payload = {"product_id": 999999, "type": "IN", "qty": 1}
        r = client.post("/api/stock/movement", json=payload)
        assert r.status_code == 404


class TestAlerts:
    def test_alerts_returns_503_when_alerts_fail_env_set(self, client):
        r = client.get("/api/stock/alerts")
        assert r.status_code == 503

    def test_alerts_returns_ok_when_env_clear(self, client):
        import httpx
        from dotenv import load_dotenv
        load_dotenv(override=True)
        os.environ.pop("ALERTS_FAIL", None)
        try:
            with httpx.Client(base_url=client.base_url, timeout=10.0) as c2:
                r = c2.get("/api/stock/alerts")
            assert r.status_code == 200
            assert isinstance(r.json(), list)
        finally:
            os.environ["ALERTS_FAIL"] = "1"
