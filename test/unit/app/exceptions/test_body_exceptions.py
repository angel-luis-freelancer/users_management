import logging
from unittest.mock import patch

from app.exceptions import (
    MissingJSONBodyException,
    InvalidJSONFormatException,
    InvalidNullValueExeption,
    SchemaValidationException
)


@patch("app.exceptions.body_exceptions.get_error_message", return_value="Mocked message")
class TestUserExceptions:

    def test_missing_json_body_exception(self, mock_get_message):
        exc = MissingJSONBodyException()
        assert exc.status_code == 400
        assert exc.log_level == logging.WARNING
        assert "expected" in exc.details
        assert "Valid JSON body" == exc.details["expected"]
        assert isinstance(exc.to_dict(), dict)
        assert mock_get_message.call_count == 2
        mock_get_message.assert_any_call('MISSING_JSON_BODY')
        mock_get_message.assert_any_call('MISSING_JSON_BODY_DETAIL')

    def test_invalid_json_format_exception(self, mock_get_message):
        exc = InvalidJSONFormatException("line 3: Unexpected token")
        assert exc.status_code == 400
        assert exc.log_level == logging.WARNING
        assert exc.details["parse_error"] == "line 3: Unexpected token"
        assert exc.details["expected"] == "Valid JSON format"
        assert isinstance(exc.to_dict(), dict)
        mock_get_message.assert_called_once_with('INVALID_JSON_FORMAT')

    def test_invalid_null_value_exception(self, mock_get_message):
        exc = InvalidNullValueExeption(["email"], ["username"])
        assert exc.status_code == 400
        assert exc.log_level == logging.WARNING
        assert "expected" in exc.details
        assert "fields_cant_be_null" in exc.details["expected"]
        assert isinstance(exc.to_dict(), dict)
        mock_get_message.assert_called_once_with('VALUE_CANT_BE_NULL')

    def test_schema_validation_exception(self, mock_get_message):
        validation_errors = [
            {
                "loc": ["email"],
                "msg": "value is not a valid email",
                "type": "value_error.email",
                "input": "bad-email"
            },
            {
                "loc": ["password"],
                "msg": "field required",
                "type": "value_error.missing",
                "input": None
            }
        ]
        exc = SchemaValidationException(validation_errors, "CreateUserSchema")
        assert exc.status_code == 400
        assert exc.log_level == logging.WARNING
        assert exc.details["error_count"] == 2
        assert exc.details["schema"] == "CreateUserSchema"
        assert isinstance(exc.to_dict(), dict)

        validation_dict = exc.to_dict()
        assert len(validation_dict["validation_errors"]) == 2
        assert validation_dict["validation_errors"][0]["field"] == "email"
        mock_get_message.assert_called_once_with('SCHEMA_VALIDATION_ERROR')