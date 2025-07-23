import pytest
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

from app.decorators import validate_query_params


class TestValidateQueryParams:
    @pytest.fixture(scope='class')
    def test_app(self):
        """Fixture para crear una app Flask específica para estos tests"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        
        # Ruta de prueba con el decorador
        @app.route('/test-endpoint')
        @validate_query_params(['username', 'uuid', 'email'])
        def test_endpoint():
            params = dict(request.args)
            return jsonify({"params": params, "message": "success"})
        
        # Ruta de prueba con diferentes parámetros permitidos
        @app.route('/test-endpoint-different')
        @validate_query_params(['id', 'name', 'status'])
        def test_endpoint_different():
            params = dict(request.args)
            return jsonify({"params": params, "message": "success"})
        
        # Ruta de prueba sin parámetros permitidos
        @app.route('/test-endpoint-no-params')
        @validate_query_params([])
        def test_endpoint_no_params():
            return jsonify({"message": "no params allowed"})
        
        return app
    
    @pytest.fixture(scope='class')
    def test_client(self, test_app):
        """Fixture para crear un cliente de prueba específico"""
        with test_app.test_client() as client:
            yield client
    
    def test_valid_single_param(self, test_client):
        """Test con un parámetro válido"""
        response = test_client.get('/test-endpoint?username=johndoe')
        assert response.status_code == 200
        assert response.json == {
            "params": {"username": "johndoe"},
            "message": "success"
        }
        

    def test_invalid_single_param(self, test_client):
        """Test con un parámetro inválido"""
        response = test_client.get('/test-endpoint?invalid_param=value')
        response_data = response.get_data(as_text=True)
        assert response.status_code == 400
        assert "Allowed parameters: username, uuid, email" in response_data
        assert "Invalids: invalid_param" in response_data
        
