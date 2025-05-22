import os
from unittest.mock import patch, MagicMock
from app import create_app

class TestApplicationStart:
    def test_create_app_default_config(self):
        """Test que la aplicación se crea con la configuración por defecto"""
        app = create_app()
        assert app is not None
        assert 'SQLALCHEMY_DATABASE_URI' in app.config
        assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False
        
    @patch.dict(os.environ, {
        'FLASK_HOST': '127.0.0.1',
        'FLASK_PORT': '8080',
        'FLASK_DEBUG': 'False'
    })
    @patch('app.create_app')
    def test_main_execution_with_env_vars(self, mock_create_app):
        """Test que la aplicación se inicia con los parámetros de entorno"""
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        from app.__main__ import main
        main()
        mock_app.run.assert_called_once_with(
            host='127.0.0.1',
            port=8080,
            debug=False
        )
