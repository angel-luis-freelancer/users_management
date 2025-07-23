import pytest

class TestValideteBodyCreateUser:
    def test_create_user_valid_body(self, client):
        """Test para crear un usuario con un body válido"""
        payload = {
            "first_name": "fernando",
            "last_name": "palomo",
            "email": "fernando@example.com",
            "phone": "111111111",
            "middle_name": "andres"
        }
        response = client.post('/api/users/', json=payload, content_type='application/json')
        data = response.get_json()

        assert response.status_code == 201
        assert data is not None
        assert "error" not in data

    def test_create_user_missing_body(self, client):
        """Test para crear un usuario sin body"""
        response = client.post('/api/users/')  
        data = response.get_json()
        
        print(f"datitaa 🤞🤞🤞 {data}")
        assert response.status_code == 400
        assert data["error"] == "Missing JSON body"
        assert data["message"] == "You must provide a valid JSON body in the request"

    def test_create_user_invalid_email(self, client):
        payload = {
            "first_name": "Carlos",
            "last_name": "Test",
            "email": "invalid-email",  # inválido
            "phone": None,
            "middle_name": None
        }
        response = client.post('/api/users/', json=payload)
        data = response.get_json()

        assert response.status_code == 400
        assert data["error"] == "Validation Error"
        assert isinstance(data["details"], list)
        assert any("email" in err["field"] for err in data["details"])