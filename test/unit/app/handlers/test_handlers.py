class TestHandlers:
    def test_custom_app_exception_handler(self, client):
        response = client.get("/raise-custom-error")
        assert response.status_code == 418
        assert response.json['error'] == "This is a test error"

    def test_404_handler(self, client):
        response = client.get("/non-existent-url")
        assert response.status_code == 404
        assert "not found" in response.json['error'].lower()

    def test_405_handler(self, client):
        response = client.post("/test-method")
        assert response.status_code == 405
        assert "not allowed" in response.json['error'].lower()

    def test_500_handler(self, client):
        response = client.get("/raise-500")
        assert response.status_code == 500
        assert "unexpected error" in response.json['error'].lower()

    def test_internal_server_error_handler(self, client):
        response = client.get("/raise-internal")
        assert response.status_code == 500
        assert "unexpected error" in response.json['error'].lower()