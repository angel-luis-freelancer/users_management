import logging
from unittest.mock import patch

from app.exceptions import (
    QueryParamException,
    MissingParameterException,
    TooManyParametersException,
    InvalidParameterException
)

@patch("app.exceptions.query_params_exceptions.get_error_message")
class TestQueryParamsExceptions:

    def test_query_param_exception_with_field(self, mock_get_msg):
        mock_get_msg.return_value = "General query param error"
        exc = QueryParamException("General query param error", 422, field="username")

        assert exc.status_code == 422
        assert exc.log_level == logging.WARNING
        assert exc.details == {"field": "username"}
        assert exc.message == "General query param error"
        assert isinstance(exc.to_dict(), dict)
        assert mock_get_msg.call_count == 0  # No se usa en este caso

    def test_query_param_exception_without_field(self, mock_get_msg):
        mock_get_msg.return_value = "General query param error"
        exc = QueryParamException("General query param error")

        assert exc.status_code == 400
        assert exc.details == {}
        assert exc.log_level == logging.WARNING
        assert isinstance(exc.to_dict(), dict)
        assert mock_get_msg.call_count == 0

    def test_missing_parameter_exception(self, mock_get_msg):
        mock_get_msg.return_value = "Falta parámetro: email"
        exc = MissingParameterException(['email'])

        assert exc.status_code == 400
        assert exc.log_level == logging.WARNING
        assert "allowed_parameters" in exc.details
        assert exc.details["allowed_parameters"] == ['email']
        assert exc.message == "Falta parámetro: email"
        assert isinstance(exc.to_dict(), dict)
        mock_get_msg.assert_called_once_with('MISSING_PARAMETER', params='email')

    def test_too_many_parameters_exception(self, mock_get_msg):
        mock_get_msg.return_value = "Demasiados parámetros: email, username"
        exc = TooManyParametersException(['email', 'username'])

        assert exc.status_code == 400
        assert exc.log_level == logging.WARNING
        assert "allowed_parameters" in exc.details
        assert exc.details["allowed_parameters"] == ['email', 'username']
        assert exc.message == "Demasiados parámetros: email, username"
        assert isinstance(exc.to_dict(), dict)
        mock_get_msg.assert_called_once_with('TOO_MANY_PARAMETERS', params='email, username')

    def test_invalid_parameter_exception(self, mock_get_msg):
        mock_get_msg.return_value = "Parámetro inválido: age"
        exc = InvalidParameterException('age', ['email', 'username'])

        assert exc.status_code == 400
        assert exc.log_level == logging.WARNING
        assert "invalid_parameter" in exc.details
        assert exc.details["invalid_parameter"] == 'age'
        assert exc.details["allowed_parameters"] == ['email', 'username']
        assert exc.message == "Parámetro inválido: age"
        assert isinstance(exc.to_dict(), dict)
        mock_get_msg.assert_called_once_with(
            'INVALID_PARAMETER',
            param='age',
            params='email, username'
        )