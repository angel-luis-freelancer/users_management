import logging
from unittest.mock import patch
from app.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    InvalidUserDataException
)

@patch('app.exceptions.user_exceptions.get_error_message')
class TestUserExceptions:

    def test_user_not_found_exception(self, mock_get_msg):
        mock_get_msg.return_value = "Usuario no encontrado"
        exc = UserNotFoundException(field='email', value='test@example.com')

        assert isinstance(exc, Exception)
        assert exc.status_code == 404
        assert exc.log_level == logging.WARNING
        assert exc.details == {
            "search_key": "email",
            "search_value": "test@example.com"
        }
        assert str(exc) == "Usuario no encontrado"

    def test_user_already_exists_exception(self, mock_get_msg):
        mock_get_msg.return_value = "Usuario ya existe"
        exc = UserAlreadyExistsException(field='username', value='angel')

        assert exc.status_code == 409
        assert exc.log_level == logging.WARNING
        assert exc.details == {
            "conflict_field": "username",
            "conflict_value": "angel"
        }
        assert str(exc) == "Usuario ya existe"

    def test_invalid_user_data_exception(self, mock_get_msg):
        mock_get_msg.return_value = "Datos inválidos"
        exc = InvalidUserDataException(field='email', value='Formato incorrecto')

        assert exc.status_code == 400
        assert exc.log_level == logging.WARNING
        assert exc.details == {
            "invalid_field": "email",
            "reason": "Formato incorrecto"
        }
        assert str(exc) == "Datos inválidos"