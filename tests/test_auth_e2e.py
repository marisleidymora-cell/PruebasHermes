import json
import urllib.request


BASE_URL = "http://127.0.0.1:8000"


def _post(path, payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}{path}", data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def _get(path, token):
    req = urllib.request.Request(f"{BASE_URL}{path}", headers={"Authorization": f"Bearer {token}"}, method="GET")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def test_login_happy_path():
    status, body = _post("/auth/login", {"username": "admin", "password": "secret123"})
    assert status == 200
    token = body["access_token"]
    status, profile = _get("/auth/me", token=token)
    assert status == 200
    assert profile["username"] == "admin"
