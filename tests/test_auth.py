import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from auth import login_user, get_user


@pytest.mark.parametrize("username,password,expected", [
    ("admin", "secret123", {"username": "admin", "role": "admin", "active": True}),
    ("user", "123456", {"username": "user", "role": "user", "active": True}),
])
def test_login_success_returns_user_data(username, password, expected):
    result = login_user(username, password)
    assert result == expected


def test_login_wrong_password_raises_auth_error():
    with pytest.raises(ValueError, match="Credenciales inválidas"):
        login_user("admin", "badpass")


def test_login_nonexistent_user_returns_none():
    result = login_user("ghost", "whatever")
    assert result is None


def test_get_user_returns_stored_user():
    user = get_user("admin")
    assert user == {"username": "admin", "role": "admin", "active": True}


def test_get_user_missing_returns_none():
    assert get_user("nope") is None
