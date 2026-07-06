import httpx
import pytest

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10.0)


@pytest.fixture(autouse=False)
def seed_clean(client: httpx.Client):
    """Fixture opcional: marcar tests que necesitan seed limpia."""
    yield
    # agregar cleanup si hace falta


def pytest_sessionfinish(session, exitstatus):
    try:
        httpx.get(f"{BASE_URL}/api/health", timeout=2)
    except Exception:
        pass
