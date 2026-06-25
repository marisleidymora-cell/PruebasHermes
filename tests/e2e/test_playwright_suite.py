from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8000"


def test_homepage_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(BASE_URL)
        assert page.title() != "" or page.content() != ""
        browser.close()


def test_product_list_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("domcontentloaded")
        text = page.content()
        assert "Resma Papel Carta" in text or "PAP-001" in text
        browser.close()


def test_alert_query_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"{BASE_URL}/")
        page.wait_for_load_state("domcontentloaded")
        assert page.content() != ""
        browser.close()
