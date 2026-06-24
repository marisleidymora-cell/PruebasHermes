_users = {
    "admin": {"password": "secret123", "username": "admin", "role": "admin", "active": True},
    "user": {"password": "123456", "username": "user", "role": "user", "active": True},
}

def login_user(username, password):
    user = _users.get(username)
    if not user:
        return None
    if user["password"] != password:
        raise ValueError("Credenciales inválidas")
    return {"username": user["username"], "role": user["role"], "active": user["active"]}

def get_user(username):
    user = _users.get(username)
    if not user:
        return None
    return {"username": user["username"], "role": user["role"], "active": user["active"]}
