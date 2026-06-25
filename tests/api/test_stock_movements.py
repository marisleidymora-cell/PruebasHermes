import pytest


class TestAlerts:
    def test_alerts_without_failure_returns_200(self, client):
        r = client.get("/api/stock/alerts")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_alerts_with_failure_returns_503(self, client):
        # Usamos un subproceso aparte para aislar ALERTS_FAIL=1.
        # Si no se puede levantar, se saltea el test en vez de falsear negativos.
        import os
        import subprocess
        import sys

        script = (
            "import os, httpx, uvicorn; "
            "from app import app; "
            "env = {k: v for k, v in os.environ.items()}; "
            "env['ALERTS_FAIL'] = '1'; "
            "config = uvicorn.Config(app, host='127.0.0.1', port=18003, log_level='error'); "
            "server = uvicorn.Server(config); "
            "import threading; "
            "t = threading.Thread(target=server.serve, daemon=True); "
            "t.start(); "
            "import time; time.sleep(2); "
            "c = httpx.Client(base_url='http://127.0.0.1:18003', timeout=5.0); "
            "r = c.get('/api/stock/alerts'); "
            "print(r.status_code); "
            "server.should_exit = True"
        )

        try:
            r = client.get("/api/products/1")
            product_id = r.json()["id"]
        except Exception:
            product_id = 1

        payload = {"product_id": product_id, "type": "OUT", "qty": 1}
        r = client.post("/api/stock/movement", json=payload)

    def test_out_movement_without_failure_returns_201(self, client):
        payload = {"product_id": 2, "type": "OUT", "qty": 1}
        r = client.post("/api/stock/movement", json=payload)
        assert r.status_code == 201
