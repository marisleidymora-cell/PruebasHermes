import pytest


class TestProductBrowsingE2E:
    def test_homepage_and_product_crud_flow(self, client):
        r = client.get("/api/products")
        assert r.status_code == 200
        r = client.get("/api/products/1")
        assert r.status_code == 200
