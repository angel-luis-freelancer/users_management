import pytest
from unittest.mock import patch
from app.controllers import UserController
from app.schemas import CreateUserSchema

class TestUsers:

    mock_user_input_necesary_data = {
        "first_name": "Micaela",
        "last_name": "Pereyra",
        "email": "mica@example.com",
    }

    mock_user_input_all_data = {
        **mock_user_input_necesary_data,
        "phone": "+34123456789",
        "middle_name": "Alejandra"
    }

    mock_user_output_necesary_data = {
        **mock_user_input_necesary_data,
        "phone": None,
        "middle_name": None,
        "status": "active",
        "username": "micaelapereyra",
        "uuid": "0abf2cf8-805d-4fb3-91c3-53840d628778"
    }

    mock_user_output_all_data = {
        **mock_user_input_all_data,
        "status": "active",
        "username": "micaelapereyra",
        "uuid": "0abf2cf8-805d-4fb3-91c3-53840d628778"
    }


    """
     ___ ___ _____   _   _ ___ ___ ___   _____ ___ ___ _____ 
    / __| __|_   _| | | | / __| __| _ \ |_   _| __/ __|_   _|
   | (_ | _|  | |   | |_| \__ \ _||   /   | | | _|\__ \ | |  
    \___|___| |_|    \___/|___/___|_|_\   |_| |___|___/ |_|                                                
    """

    def test_get_user_no_params(self, client):
        """Test cuando no se envían parámetros"""
        response = client.get('/api/users/')
        
        assert response.status_code == 400
        assert response.json == {"error": "we need the parameter uuid, email or username"}

    def test_get_user_too_many_params(self, client):
        """Test cuando se envían múltiples parámetros"""
        response = client.get('/api/users/?username=johndoe&email=john@example.com')
        
        assert response.status_code == 400
        assert response.json == {"error": "too many parameters, only admited 1"}

    @patch.object(UserController, 'get_user')
    def test_get_user_by_username(self, mock_get_user, client):
        """Test búsqueda por username exitosa"""
        mock_get_user.return_value = self.mock_user_input_all_data
        response = client.get(f"/api/users/?username={self.mock_user_output_all_data['username']}")

        assert response.status_code == 200
        assert response.json == self.mock_user_input_all_data
        mock_get_user.assert_called_once_with('username', self.mock_user_output_all_data['username'])

    @patch.object(UserController, 'get_user')
    def test_get_user_by_email(self, mock_get_user, client):
        """Test búsqueda por email exitosa"""
        mock_get_user.return_value = self.mock_user_input_all_data
        response = client.get(f"/api/users/?email={self.mock_user_input_all_data['email']}")
        
        assert response.status_code == 200
        assert response.json == self.mock_user_input_all_data
        mock_get_user.assert_called_once_with('email', self.mock_user_output_all_data["email"])

    @patch.object(UserController, 'get_user')
    def test_get_user_by_uuid(self, mock_get_user, client):
        """Test búsqueda por uuid exitosa"""
        mock_get_user.return_value = self.mock_user_input_all_data
        response = client.get(f"/api/users/?uuid={self.mock_user_output_all_data['uuid']}")
        
        assert response.status_code == 200
        assert response.json == self.mock_user_input_all_data
        mock_get_user.assert_called_once_with('uuid', self.mock_user_output_all_data['uuid'])

    @patch.object(UserController, 'get_user')
    def test_get_user_value_error_exception(self, mock_get_user, client):
        """Test cuando UserController.get_user lanza ValueError"""
        error_message = "Catastrofe error"
        mock_get_user.side_effect = ValueError(error_message)
        response = client.get(f"/api/users/?username={self.mock_user_output_all_data['username']}")

        assert response.status_code == 400
        assert response.json == {"error": error_message}
        mock_get_user.assert_called_once_with('username', self.mock_user_output_all_data['username'])


    """
     ___ ___ ___    _ _____ ___   _   _ ___ ___ ___   _____ ___ ___ _____ 
    / __| _ \ __|  /_\_   _| __| | | | / __| __| _ \ |_   _| __/ __|_   _|
    | (__|   / _| / _ \| | | _|  | |_| \__ \ _||   /   | | | _|\__ \ | |  
     \___|_|_\___/_/ \_\_| |___| \___/ |___/___|_|_\   |_| |___|___/ |_|  
    """

    def test_create_user_all_data(self, client):
        """Test que verifica la estructura de entrada/salida sin lógica de negocio"""
        with patch(
            'app.controllers.users.UserController.create_user', 
            return_value=self.mock_user_output_all_data
        ) as mock_create:
            response = client.post('/api/users/', json=self.mock_user_input_all_data)

            assert response.status_code == 201
            assert response.json == self.mock_user_output_all_data
            mock_create.assert_called_once_with(self.mock_user_input_all_data)


    def test_create_user_necesary_data(self, client):
        """Test que verifica la estructura de entrada/salida sin lógica de negocio"""
        with patch(
            'app.controllers.users.UserController.create_user', 
            return_value=self.mock_user_output_necesary_data
        ):
            response = client.post('/api/users/', json=self.mock_user_input_necesary_data)

            assert response.status_code == 201
            assert response.json == self.mock_user_output_necesary_data


    @pytest.mark.parametrize("missing_field", ["first_name", "last_name", "email"])
    def test_missing_required_fields(self, client, missing_field):
        """Test que verifica campos requeridos faltantes"""
        test_data = self.mock_user_input_all_data.copy()
        test_data.pop(missing_field)
        
        response = client.post('/api/users/', json=test_data)
        
        assert response.status_code == 400
        assert response.json['error'] == 'Validation Error'
        assert response.json['details'][0]['field'] == missing_field
        assert response.json['details'][0]['type'] == 'missing'
    #    assert missing_field in response.json["error"].lower()

    @patch.object(UserController, 'create_user')
    def test_create_user_value_error_exception(self, mock_create_user, client):
        """Test cuando UserController.create_user lanza ValueError"""
        error_message = "Catastrofe error"
        mock_create_user.side_effect = ValueError(error_message)
        response = client.post(f"/api/users/", json=self.mock_user_input_necesary_data)
        expected_data = {
            'first_name': 'Micaela',
            'middle_name': None, 
            'last_name': 'Pereyra',
            'email': 'mica@example.com',
            'phone': None
        }
        assert response.status_code == 400
        assert response.json == {"error": error_message}
        mock_create_user.assert_called_once_with(expected_data)