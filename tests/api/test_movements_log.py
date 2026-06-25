class TestMovementsLog:
    def test_movements_returns_list(self, client):
        r = client.get("/api/movements")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        # Newest first (by id descending due to ORDER BY id DESC)
        if len(data) > 1:
            assert data[0]["id"] >= data[1]["id"]
