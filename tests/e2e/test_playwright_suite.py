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
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(f"{BASE_URL}/", wait_until="domcontentloaded")
        assert page.content() != ""
        write_allure_screenshot(page, "alerts_flow")
        time.sleep(2)
        browser.close()
