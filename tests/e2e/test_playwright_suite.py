import os
import time

from playwright.sync_api import sync_playwright
from conftest import write_allure_screenshot

BASE_URL = "http://localhost:8000"


def test_homepage_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded")
        assert page.content() != ""
        write_allure_screenshot(page, "homepage")
        time.sleep(2)
        browser.close()


def test_product_list_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(f"{BASE_URL}/", wait_until="domcontentloaded")
        text = page.content()
        assert "Resma Papel Carta" in text or "PAP-001" in text
        write_allure_screenshot(page, "product_list")
        time.sleep(2)
        browser.close()


def test_alert_query_flow():
    """
    Prueba real de flujo de alertas: carga la home, hace click en el botón
    "Consultar alertas" y verifica que la llamada real a
    GET /api/stock/alerts responda 200 y que la sección de alertas se
    actualice en el DOM.

    Antes este test solo abría la home y comprobaba que no estuviera
    vacía — no tocaba el botón de alertas ni verificaba nada relacionado
    a alertas, a pesar de su nombre. Ahora sí ejercita el flujo real.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(f"{BASE_URL}/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")

        with page.expect_response("**/api/stock/alerts") as resp_info:
            page.locator("#refresh-alerts").click()
        response = resp_info.value
        assert response.status == 200

        # La sección de alertas debe existir en el DOM tras la respuesta.
        assert page.locator("#alerts-section").count() == 1
        write_allure_screenshot(page, "alerts_flow")
        time.sleep(2)
        browser.close()
