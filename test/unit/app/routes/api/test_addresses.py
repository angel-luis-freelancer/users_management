import pytest
import json
from unittest.mock import patch, MagicMock
from flask import Flask

from app.routes.api.addresses import addresses_bp

class TestAddresses:
    """
    _____ _____ _____    _____ ____  ____  _____ _____ _____ _____ _____ _____ _____    _____ _____ _____ _____ 
    |   __|   __|_   _|  |  _  |    \|    \| __  |   __|   __|   __|   __|   __|   __|  |_   _|   __|   __|_   _|
    |  |  |   __| | |    |     |  |  |  |  |    -|   __|__   |__   |   __|__   |__   |    | | |   __|__   | | |  
    |_____|_____| |_|    |__|__|____/|____/|__|__|_____|_____|_____|_____|_____|_____|    |_| |_____|_____| |_|  
    """
    @pytest.mark.parametrize("query_param,param_value", [
    ('email', 'email@example.com'),
    ('username', 'testuser')])
    @patch('app.routes.api.addresses.AddressController.get_user_address')
    def test_get_users_address_by_email_success(self, mock_controller, client, sample_user, sample_address, query_param, param_value):
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
        if query_param == 'email':
            param_value = sample_user.email 
        else:
            param_value = sample_user.username 
        response = client.get(f'/api/addresses/user?{query_param}={param_value}')
        data = response.get_json()
        
        assert response.status_code == 200
        assert len(data) == 2
        assert data['addresses'][0]['street'] == 'Calle Falsa'
        assert data['metadata']['username'] == sample_user.username
        mock_controller.assert_called_once_with(query_param, param_value)

    def test_get_users_address_no_parameters(self, client):
        """Test: Error por falta de parámetros"""
        response = client.get('/api/addresses/user')
        
        assert response.status_code == 400
        assert response.get_json() == {"error": "we need the parameters email or username"}

    def test_get_users_address_too_many_parameters(self, client):
        """Test: Error por demasiados parámetros"""
        response = client.get('/api/addresses/user?email=test@test.com&username=testuser')
        
        assert response.status_code == 400
        assert response.get_json() == {"error": "too many parameters, only admited 1"}

    def test_get_users_address_invalid_parameter(self, client):
        """Test: Error por parámetro inválido (decorador validate_query_params)"""
        response = client.get('/api/addresses/user?invalid_param=test')
        
        assert response.status_code == 400

    @patch('app.routes.api.addresses.AddressController.get_user_address')
    def test_get_users_address_controller_error(self, mock_controller, client):
        """Test: Error del controlador"""
        mock_controller.side_effect = ValueError("Database error")
        
        response = client.get('/api/addresses/user?email=test@test.com')
        
        assert response.status_code == 400
        assert "Database error" in response.get_json()["error"]

    @patch('app.routes.api.addresses.AddressController.get_user_address')
    def test_get_users_address_empty_parameter_value(self, mock_controller, client):
        """Test: Parámetro con valor vacío"""
        mock_controller.side_effect = ValueError("User dosent exists")
        
        response = client.get('/api/addresses/user?email=')
        
        assert response.status_code == 400
        assert "User dosent exists" in response.get_json()["error"]

    
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

    def test_create_users_address_no_parameters(self, client):
        """Test: Error por falta de parámetros"""
        response = client.post('/api/addresses/', json={"country": "country"}, content_type='application/json')
        assert response.status_code == 400
        assert response.get_json() == {"error": "we need the parameters email or username"}

    def test_create_users_address_too_many_parameters(self, client):
        response = client.post('/api/addresses/?email=test@test.com&username=testuser', json={"country": "country"}, content_type='application/json')
        assert response.status_code == 400
        assert response.get_json() == {"error": "too many parameters, only admited 1"}