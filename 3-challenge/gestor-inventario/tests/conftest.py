"""Fixtures compartidos para la suite de pruebas API."""
import uuid

import httpx
import pytest

BASE_URL = "http://localhost:8000"


@pytest.fixture
def client():
    """Cliente HTTP sincrono para las pruebas."""
    with httpx.Client(base_url=BASE_URL, timeout=10.0) as c:
        yield c


@pytest.fixture
def sample_product(client):
    """Crea un producto de prueba y retorna sus datos."""
    sku = f"QA-{uuid.uuid4().hex[:8].upper()}"
    payload = {
        "name": "Producto QA Test",
        "sku": sku,
        "cost_cents": 10000,
        "price_cents": 15000,
        "stock": 100,
        "min_stock": 10,
        "supplier_id": 1,
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201
    return response.json()
