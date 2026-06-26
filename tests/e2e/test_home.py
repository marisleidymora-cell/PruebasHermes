import httpx
import pytest

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL.rstrip("/")


@pytest.fixture(scope="session")
def frontend_client(base_url):
    return httpx.Client(base_url=base_url, timeout=10.0)


class TestHomePage:
    def test_frontend_responds(self, frontend_client):
        r = frontend_client.get("/")
        assert r.status_code == 200
