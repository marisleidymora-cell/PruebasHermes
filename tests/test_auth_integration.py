import json
import urllib.request


BASE_URL = "http://127.0.0.1:8000"


def _post(path, payload, token=None):
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{BASE_URL}{path}", data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _get(path, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{BASE_URL}{path}", headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def test_login_returns_token_for_valid_user():
    status, body = _post("/auth/login", {"username": "admin", "password": "secret123"})
    assert status == 200
    assert "access_token" in body


def test_login_returns_401_for_invalid_password():
    status, body = _post("/auth/login", {"username": "admin", "password": "bad"})
    assert status == 401
    assert body.get("error") == "invalid_credentials"


def test_authenticated_request_returns_user_info():
    _, login = _post("/auth/login", {"username": "user", "password": "123456"})
    token = login["access_token"]
    status, body = _get("/auth/me", token=token)
    assert status == 200
    assert body.get("username") == "user"


def test_authenticated_request_without_token_returns_401():
    status, body = _get("/auth/me")
    assert status == 401
