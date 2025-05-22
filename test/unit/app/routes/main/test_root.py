def test_home_route(client):
    """Test para el endpoint ping"""
    response = client.get('/ping')
    assert response.status_code == 200