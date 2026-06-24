import urllib.request
import json


BASE_URL = "http://localhost:8000"


def request(path, token=None, payload=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=headers, method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return resp.status, body


def test_login_returns_token_for_valid_user():
    status, body = request("/auth/login", payload={"username": "admin", "password": "secret123"})
    assert status == 200
    assert "access_token" in body


def test_login_returns_401_for_invalid_password():
    status, body = request("/auth/login", payload={"username": "admin", "password": "bad"})
    assert status == 401
    assert body.get("error") == "invalid_credentials"


def test_authenticated_request_returns_user_info():
    _, login = request("/auth/login", payload={"username": "user", "password": "123456"})
    token = login["access_token"]
    status, body = request("/auth/me", token=token)
    assert status == 200
    assert body["username"] == "user"


def test_authenticated_request_without_token_returns_401():
    status, body = request("/auth/me")
    assert status == 401
