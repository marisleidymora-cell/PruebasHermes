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
        finally:
            browser.close()


def _start_alerts_fail_server(port: int = 18003):
    import os
    import subprocess
    import sys
    import time
    import tempfile
    from pathlib import Path
    from urllib.request import urlopen

    env = os.environ.copy()
    env["ALERTS_FAIL"] = "1"
    sut_dir = Path.home() / "Desktop" / "reto-ai-first-fase1" / "reto-ai-first-fase1" / "3-challenge" / "gestor-inventario"
    fd, script_path = tempfile.mkstemp(suffix=".py", prefix=f"sut_alerts_{port}_")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(
                f"import os\n"
                f"os.chdir({str(sut_dir)!r})\n"
                f"import sys\n"
                f"sys.path.insert(0, str({str(sut_dir)!r}))\n"
                f"from app import app\n"
                f"import uvicorn\n"
                f"config = uvicorn.Config(app, host='127.0.0.1', port={port}, log_level='error')\n"
                f"server = uvicorn.Server(config)\n"
                f"server.run()\n"
            )
        python = sys.executable
        proc = subprocess.Popen(
            [python, script_path],
            cwd=str(sut_dir),
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        url = f"http://127.0.0.1:{port}/api/health"
        for _ in range(50):
            try:
                urlopen(url, timeout=0.3)
                return proc, port
            except Exception:
                time.sleep(0.25)
        proc.terminate()
        raise RuntimeError(f"No se pudo levantar servidor ALERTS_FAIL=1 en puerto {port}")
    except Exception:
        raise
    finally:
        try:
            Path(script_path).unlink()
        except Exception:
            pass


def test_alerts_section_shows_503_when_alert_service_down():
    server, port = _start_alerts_fail_server(18003)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
            page = browser.new_page()
            try:
                page.goto(f"http://localhost:{port}/", wait_until="domcontentloaded")
                page.wait_for_load_state("networkidle")

                with page.expect_response("**/api/stock/alerts") as resp_info:
                    page.locator("#refresh-alerts").click()
                response = resp_info.value
                assert response.status == 503
            finally:
                browser.close()
    finally:
        server.terminate()
