import os
import importlib
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
ALERTS_FAIL = os.getenv("ALERTS_FAIL", "0")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL.rstrip("/")


@pytest.fixture(scope="session")
def client(base_url):
    import httpx
    return httpx.Client(base_url=base_url, timeout=10.0)


@pytest.fixture
def fresh_client(base_url):
    import httpx
    with httpx.Client(base_url=base_url, timeout=10.0) as c:
        yield c


def _allure_attach_text(name, body):
    try:
        allure = importlib.import_module("allure")
        allure.attach(body, name=name, attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass


def write_allure_screenshot(page, name="screenshot"):
    try:
        allure = importlib.import_module("allure")
        allure.attach(page.screenshot(full_page=True), name=name, attachment_type=allure.attachment_type.PNG)
    except Exception:
        pass


def _clean_allure_results(path="/Users/admin/Desktop/PruebasHermes-trackQA/allure-results"):
    try:
        import shutil
        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    _clean_allure_results()
