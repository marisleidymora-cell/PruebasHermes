import importlib.util
import os
import socket
import sys

import httpx
import pytest
import uvicorn

SUT_APP_PATH = os.path.abspath(
    "/Users/admin/Desktop/reto-ai-first-fase1/reto-ai-first-fase1/3-challenge/gestor-inventario/app.py"
)


def _find_app():
    sys.path.insert(0, os.path.dirname(SUT_APP_PATH))
    spec = importlib.util.spec_from_file_location("app", SUT_APP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {SUT_APP_PATH}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.app


def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="session")
def failed_alerts_client():
    app = _find_app()
    port = _free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    old = os.environ.get("ALERTS_FAIL")
    os.environ["ALERTS_FAIL"] = "1"
    t = __import__("threading").Thread(target=server.serve, daemon=True)
    t.start()
    import time
    time.sleep(2)
    c = httpx.Client(base_url=f"http://127.0.0.1:{port}", timeout=5.0)
    yield c
    c.close()
    if old is None:
        os.environ.pop("ALERTS_FAIL", None)
    else:
        os.environ["ALERTS_FAIL"] = old


def test_alerts_endpoint_returns_503(failed_alerts_client):
    r = failed_alerts_client.get("/api/stock/alerts")
    assert r.status_code == 503


def test_out_movement_returns_503_when_alerts_down(failed_alerts_client):
    r = failed_alerts_client.post("/api/stock/movement", json={
        "product_id": 1,
        "type": "OUT",
        "qty": 1,
        "notes": "QA",
    })
    assert r.status_code == 503
