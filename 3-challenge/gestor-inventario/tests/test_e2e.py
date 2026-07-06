import os, sys, subprocess, time
from pathlib import Path

APP_DIR = Path("/tmp/reto-ai-first-fase1/3-challenge/gestor-inventario")
DB_FILE = APP_DIR / "e2e.db"

os.environ["DB_PATH"] = str(DB_FILE)
os.environ["ALERTS_FAIL"] = "0"

server = subprocess.Popen(
    ["python3", "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=str(APP_DIR),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)
try:
    time.sleep(3)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/")
        assert "Gestor de Inventario" in page.title()
        page.wait_for_selector("table")
        products = page.query_selector_all("tbody tr")
        assert len(products) >= 1
        page.select_option("#mov-product", "1")
        page.select_option("#mov-type", "IN")
        page.fill("#mov-qty", "5")
        page.click("button[type=submit]")
        time.sleep(1)
        alerts_btn = page.query_selector("#refresh-alerts")
        if alerts_btn:
            alerts_btn.click()
            time.sleep(1)
        browser.close()
    print("e2e ok")
finally:
    server.terminate()
    server.wait(timeout=10)
    if DB_FILE.exists():
        DB_FILE.unlink()
