import os

import pytest
from playwright.sync_api import Page, expect


BASE_URL = os.environ.get("QA_BASE_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1366, "height": 900},
    }


def test_home_loads_and_api_health(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title("Gestor de Inventario")
    r = page.evaluate("""async () => {
      const res = await fetch('/api/health');
      return {status: res.status, data: await res.json()};
    }""")
    assert r["status"] == 200
    assert r["data"] == {"status": "ok"}


def test_load_products_and_register_movement(page: Page):
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")

    # Log consola para depuración si algo falla
    console = []
    page.on("console", lambda msg: console.append(f"{msg.type}: {msg.text}"))

    # Esperar al API en lugar del render del DOM para evitar flakiness de timing
    products = page.evaluate("""async () => {
      const res = await fetch('/api/products');
      return res.ok ? await res.json() : [];
    }""")
    assert len(products) >= 1

    # Registrar movimiento desde el browser
    r = page.evaluate("""async () => {
      const res = await fetch('/api/products');
      const products = await res.json();
      const body = {
        product_id: products[0].id,
        type: 'IN',
        qty: 3,
        notes: 'QA e2e',
      };
      const mov = await fetch('/api/stock/movement', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body),
      });
      return {status: mov.status, data: await mov.json()};
    }""")

    assert r["status"] == 201
    data = r["data"]
    assert data["type"] == "IN"
    assert data["qty"] == 3
    assert data["product_id"] == products[0]["id"]

    # Validar stock actualizado
    refreshed = page.evaluate("""async () => {
      const res = await fetch('/api/products');
      return res.ok ? await res.json() : [];
    }""")
    refreshed_product = next(p for p in refreshed if p["id"] == products[0]["id"])
    assert refreshed_product["stock"] == products[0]["stock"] + 3


def test_alerts_query_ui(page: Page):
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")
    expect(page.locator("#refresh-alerts")).to_be_enabled()
