import pytest


class TestHomePage:
    def test_frontend_responds(self, frontend_client):
        r = frontend_client.get("/")
        assert r.status_code == 200
