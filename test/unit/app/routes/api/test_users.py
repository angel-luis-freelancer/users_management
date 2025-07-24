from flask import json
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
    mock_user_update_payload = {"middle_name": "Isabela"}

    mock_user_updated_data = {
            "fields_updated": [["middle_name", "Isabela"]],
            "identifier": {"username": "anatorres"}
        }

    """
       __            __                __                         
      / /____  _____/ /_   ____ ____  / /_   __  __________  _____
     / __/ _ \/ ___/ __/  / __ `/ _ \/ __/  / / / / ___/ _ \/ ___/
    / /_/  __(__  ) /_   / /_/ /  __/ /_   / /_/ (__  )  __/ /    
    \__/\___/____/\__/   \__, /\___/\__/   \__,_/____/\___/_/     
                        /____/                                                                             
    """

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
    def test_get_user_value_error_exception(self, mock_get_user, client):
        """Test cuando UserController.get_user lanza ValueError"""
        error_message = "Catastrofe error"
        mock_get_user.side_effect = ValueError(error_message)
        response = client.get(f"/api/users/?username={self.mock_user_output_all_data['username']}")

        assert response.status_code == 400
        assert response.json == {"error": error_message}
        mock_get_user.assert_called_once_with('username', self.mock_user_output_all_data['username'])


    """
       __            __                          __                                   
      / /____  _____/ /_   _____________  ____ _/ /____     __  __________  _____
     / __/ _ \/ ___/ __/  / ___/ ___/ _ \/ __ `/ __/ _ \   / / / / ___/ _ \/ ___/
    / /_/  __(__  ) /_   / /__/ /  /  __/ /_/ / /_/  __/  / /_/ (__  )  __/ /  
    \__/\___/____/\__/   \___/_/   \___/\__,_/\__/\___/   \__,_/____/\___/_/                                                                                       
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

    """
       __            __                     __      __                              
      / /____  _____/ /_   __  ______  ____/ /___ _/ /____     __  __________  _____
     / __/ _ \/ ___/ __/  / / / / __ \/ __  / __ `/ __/ _ \   / / / / ___/ _ \/ ___/
    / /_/  __(__  ) /_   / /_/ / /_/ / /_/ / /_/ / /_/  __/  / /_/ (__  )  __/ /    
    \__/\___/____/\__/   \__,_/ .___/\__,_/\__,_/\__/\___/   \__,_/____/\___/_/     
                             /_/                                                    
    """

    def test_update_user_data(self, client, sample_user):
        """Test update de user por username exitosa"""

        with patch(
            'app.controllers.users.UserController.update_user', 
            return_value=self.mock_user_updated_data
        ):
            response = client.patch(f'/api/users/update?username={sample_user.username}', 
                                    json=self.mock_user_update_payload, content_type='application/json')

            assert response.status_code == 200
            assert response.json == self.mock_user_updated_data


    @patch.object(UserController, 'update_user')
    def test_update_user_value_error_exception(self, mock_update_user, client, sample_user):
        """Test cuando UserController.update_user lanza ValueError"""
        error_message = "Catastrofe error"
        mock_update_user.side_effect = ValueError(error_message)
        excepted_data = {'first_name': None, 'middle_name': 'Isabela', 'last_name': None, 'phone': None}
        response = client.patch(f"/api/users/update?username={sample_user.username}", json=self.mock_user_update_payload)
        assert response.status_code == 400
        assert response.json == {"error": error_message}
        mock_update_user.assert_called_once_with('username', sample_user.username, excepted_data   )