"""
Smoke tests de disponibilidad del frontend estático y del listado de
productos vía HTTP simple (sin navegador).

Nota de reclasificación: estas pruebas antes vivían en `tests/e2e/` bajo
los nombres `test_home.py` y `test_frontend_flow.py`, pero usan httpx
(peticiones HTTP directas), no un navegador real. No son E2E de verdad
(no abren Chromium, no interactúan con la página) — son smoke tests de API
que duplicaban cobertura de `tests/api/test_api_contract.py`. Se movieron
aquí para que el conteo de "pruebas E2E" refleje solo pruebas que
realmente abren un navegador.
"""
import httpx
import pytest

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def frontend_client():
    return httpx.Client(base_url=BASE_URL, timeout=10.0)


class TestFrontendSmoke:
    def test_home_page_responds_200(self, frontend_client):
        """La home estática (`/`) debe responder 200."""
        r = frontend_client.get("/")
        assert r.status_code == 200

    def test_products_endpoint_reachable_from_frontend_client(self, frontend_client):
        """El listado de productos debe ser alcanzable con un cliente HTTP simple."""
        r = frontend_client.get("/api/products")
        assert r.status_code == 200
        r = frontend_client.get("/api/products/1")
        assert r.status_code == 200
