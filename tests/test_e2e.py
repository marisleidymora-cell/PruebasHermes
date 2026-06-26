import pytest
from playwright.sync_api import sync_playwright
import subprocess
import time
import os
import signal
import sys

# Server setup
server_process = None

def start_server():
    global server_process
    env = os.environ.copy()
    env["DB_PATH"] = "/tmp/test_e2e_inventario.db"
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="/Users/jk-0026/reto-ai-first-fase1/3-challenge/gestor-inventario",
        env=env
    )
    time.sleep(2)  # Wait for server startup

def stop_server():
    global server_process
    if server_process:
        server_process.terminate()
        server_process.wait()
        server_process = None


# ========== UI Tests ==========

def test_ui_loads_products():
    """Test that the UI loads and displays products"""
    start_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8001")
            
            # Wait for products to load
            page.wait_for_selector("table tbody tr", timeout=5000)
            
            # Should have multiple product rows
            rows = page.query_selector_all("table tbody tr")
            assert len(rows) >= 6
            
            # Check that product names are displayed
            first_row_text = page.inner_text("table tbody tr:first-child")
            assert "PAP-001" in first_row_text
            
            browser.close()
    finally:
        stop_server()


def test_ui_register_movement():
    """Test registering stock movement via UI"""
    start_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8001")
            
            # Get initial stock value
            page.wait_for_selector('[data-stock="1"]', timeout=5000)
            initial_stock = int(page.inner_text('[data-stock="1"]'))
            
            # Fill and submit movement form
            page.select_option("#mov-product", "1")
            page.select_option("#mov-type", "IN")
            page.fill("#mov-qty", "5")
            page.fill("#mov-notes", "Test E2E")
            page.click('button[type="submit"]')
            
            # Wait for result
            page.wait_for_selector("#result.ok", timeout=5000)
            
            # Verify stock increased
            updated_stock = int(page.inner_text('[data-stock="1"]'))
            assert updated_stock == initial_stock + 5
            
            browser.close()
    finally:
        stop_server()


def test_ui_check_alerts():
    """Test checking stock alerts via UI"""
    start_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8001")
            
            # Click alerts button
            page.click("#refresh-alerts")
            
            # Wait for alerts section
            page.wait_for_selector(".alerts-section", timeout=5000)
            
            # Verify alerts section shows content (products or no-alerts message or table)
            alerts_html = page.inner_html(".alerts-section")
            # Should contain either table, no-alerts message, or product rows
            assert len(alerts_html) > 0  # Section has content
            
            browser.close()
    finally:
        stop_server()


def test_ui_negative_stock_flow():
    """E2E test: Verify negative stock defect is reproducible via UI"""
    start_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("http://localhost:8001")
            
            page.wait_for_selector('[data-stock="1"]', timeout=5000)
            
            # Try to make stock negative via OUT
            page.select_option("#mov-product", "1")
            page.select_option("#mov-type", "OUT")
            page.fill("#mov-qty", "99999")
            page.click('button[type="submit"]')
            
            page.wait_for_selector("#result.ok", timeout=5000)
            
            # Check stock is now negative
            stock_text = page.inner_text('[data-stock="1"]')
            stock_value = int(stock_text)
            assert stock_value < 0  # Defect confirmed via UI
            
            browser.close()
    finally:
        stop_server()