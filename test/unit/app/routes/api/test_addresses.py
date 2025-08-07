import pytest
import json
from unittest.mock import patch

from app.routes.api.addresses import addresses_bp

class TestAddresses:
    """
       __            __                __               __    __                   
      / /____  _____/ /_   ____ ____  / /_   ____ _____/ /___/ /_______  __________
     / __/ _ \/ ___/ __/  / __ `/ _ \/ __/  / __ `/ __  / __  / ___/ _ \/ ___/ ___/
    / /_/  __(__  ) /_   / /_/ /  __/ /_   / /_/ / /_/ / /_/ / /  /  __(__  |__  ) 
    \__/\___/____/\__/   \__, /\___/\__/   \__,_/\__,_/\__,_/_/   \___/____/____/  
                        /____/                                                     
    """
    @pytest.mark.parametrize("param_key, param_value", [
    ('email', 'email@example.com'),
    ('username', 'testuser')])
    @patch('app.routes.api.addresses.AddressController.get_user_address')
    def test_get_users_address_by_email_success(self, mock_controller, client, sample_user, sample_address, param_key, param_value):
        """Test: Obtener direcciones por email u por username exitosamente"""
        mock_controller.return_value = {
            "addresses": [
                {
                    'city': 'Springfield',
                    'country': 'USA',
                    'instructions': 'Casa azul con portón blanco',
                    'number': 123,
                    'street': 'Calle Falsa',
                    'state': 'Illinois',
                }],
            "metadata": {
                "length": 1,
                "username": sample_user.username
            }
        }
        if param_key == 'email':
            param_value = sample_user.email 
        else:
            param_value = sample_user.username 
        response = client.get(f'/api/addresses/user?{param_key}={param_value}')
        data = response.get_json()
        
        assert response.status_code == 200
        assert len(data) == 2
        assert data['addresses'][0]['street'] == 'Calle Falsa'
        assert data['metadata']['username'] == sample_user.username
        mock_controller.assert_called_once_with(param_key, param_value)


    """
       __            __                          __                    __    __                   
      / /____  _____/ /_   _____________  ____ _/ /____     ____ _____/ /___/ /_______  __________
     / __/ _ \/ ___/ __/  / ___/ ___/ _ \/ __ `/ __/ _ \   / __ `/ __  / __  / ___/ _ \/ ___/ ___/
    / /_/  __(__  ) /_   / /__/ /  /  __/ /_/ / /_/  __/  / /_/ / /_/ / /_/ / /  /  __(__  |__  ) 
    \__/\___/____/\__/   \___/_/   \___/\__,_/\__/\___/   \__,_/\__,_/\__,_/_/   \___/____/____/  
    """

    @patch('app.routes.api.addresses.AddressController.create_address')
    def test_create_address_success(self, mock_controller, client, sample_user):
        """Test: Crear dirección exitosamente"""
        # Mock del controlador
        address_response = {
            'username': sample_user.username,
            'street': None,
            'number': None,
            'city': None,
            'state': None,
            'country': 'Nuevo País',
        }
        mock_controller.return_value = address_response
        address_data = {'country': 'Nuevo País'}  
        response = client.post(
            f'/api/addresses/?email={sample_user.email}',
            data=json.dumps(address_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.get_json() == address_response
