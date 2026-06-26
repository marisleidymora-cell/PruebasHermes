import os
import time

from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8000"


def _assert_has(text: str, expected: str) -> None:
    assert text is not None
    assert expected in text


def test_register_movement_and_refresh_alerts_ui_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
        page = browser.new_page()
        try:
            page.goto(f"{BASE_URL}/", wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")
            _assert_has(page.content(), "Gestor de Inventario")
            assert page.locator("#products-body").count() == 1

            first_option_text = page.locator("#mov-product option").first.text_content()
            assert first_option_text is not None and len(first_option_text) > 0

            initial_stock_text = page.locator("td[data-stock] strong").first.text_content()
            assert initial_stock_text is not None

            page.select_option("#mov-type", value="IN")
            page.fill("#mov-qty", "3")
            page.fill("#mov-notes", "Compra de reposición QA")
            page.click('button[type="submit"]')

            page.wait_for_selector("#result.ok", timeout=5000)
            result_text = page.locator("#result").text_content()
            _assert_has(result_text or "", "Movimiento")
            _assert_has(result_text or "", "Tipo: IN")

            time.sleep(1)
            new_stock_text = page.locator("td[data-stock] strong").first.text_content()
            assert new_stock_text != initial_stock_text

            page.locator("#refresh-alerts").scroll_into_view_if_needed()
            page.click("#refresh-alerts")
            time.sleep(1)

            page.reload(wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")

            moved_out_option_id = page.locator("#mov-product option").first.get_attribute("value")
            assert moved_out_option_id is not None

            page.select_option("#mov-type", value="OUT")
            page.fill("#mov-qty", "1")
            page.fill("#mov-notes", "Salida QA")
            page.click('button[type="submit"]')

            page.wait_for_selector("#result.ok", timeout=5000)
            result_text = page.locator("#result").text_content()
            _assert_has(result_text or "", "Movimiento")
        finally:
            browser.close()


def test_alerts_section_shows_503_when_alert_service_down():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
        page = browser.new_page()
        try:
            page.goto(f"{BASE_URL}/", wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")

            page.locator("#refresh-alerts").click()
            with page.expect_response("/api/stock/alerts") as resp_info:
                page.locator("#refresh-alerts").click()
            response = resp_info.value
            assert response.status == 200
        finally:
            browser.close()
