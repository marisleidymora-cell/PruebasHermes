class TestMovementsLog:
    def test_movements_returns_array_and_ordered_desc(self, client):
        r = client.get("/api/movements")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        if len(data) > 1:
            assert data[0]["id"] >= data[1]["id"]
