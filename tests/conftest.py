import os
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
