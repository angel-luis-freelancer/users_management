import pytest

class TestQueryParams:

    def test_valid_email_param(self, client):
        response = client.get("/api/test-user-query/?email=test@example.com")
        assert response.status_code == 200

    def test_missing_query_param(self, client):
        response = client.get("/api/test-user-query/")
        assert response.status_code == 400

    def test_too_many_query_params(self, client):
        response = client.get("/api/test-user-query/?email=test@example.com&username=testuser")
        assert response.status_code == 400

    def test_invalid_query_param(self, client):
        response = client.get("/api/test-user-query/?invalid=test")
        assert response.status_code == 400