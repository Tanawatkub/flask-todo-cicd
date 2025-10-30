def test_404_not_found(client):
    res = client.get("/nonexistent")
    assert res.status_code == 404
    assert "error" in res.json
