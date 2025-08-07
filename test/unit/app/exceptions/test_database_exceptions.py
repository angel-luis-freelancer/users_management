import logging
from unittest.mock import patch

from app.exceptions.database_exceptions import DatabaseException

@patch("app.exceptions.database_exceptions.get_error_message", return_value="Mocked DB error")
class TestUserExceptions:

    def test_database_exception_with_error(self, mock_get_msg):
        original_error = 'IntegrityError: duplicate key'
        exc = DatabaseException(original_error)

        assert exc.status_code == 500
        assert exc.log_level == logging.ERROR
        assert exc.message == "Mocked DB error"
        assert "original_error" in exc.details
        assert "duplicate key" in exc.details["original_error"]
        assert isinstance(exc.to_dict(), dict)
        assert mock_get_msg.call_count == 1

    def test_database_exception_without_error(self, mock_get_msg):
        exc = DatabaseException()

        assert exc.status_code == 500
        assert exc.log_level == logging.ERROR
        assert exc.message == "Mocked DB error"
        assert exc.details == {}  # No error enviado
        assert isinstance(exc.to_dict(), dict)
        assert mock_get_msg.call_count == 1