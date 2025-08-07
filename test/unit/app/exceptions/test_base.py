from datetime import datetime
import logging
from unittest.mock import MagicMock

from app.exceptions.base import BaseAppException

class TestExceptionBase:
    def test_init_sets_all_attributes(self):
        message = "Test error"
        status_code = 400
        details = {"field": "invalid"}
        log_level = logging.WARNING
        exc = BaseAppException(message, status_code, details, log_level)

        assert exc.message == message
        assert exc.status_code == status_code
        assert exc.details == details
        assert exc.log_level == log_level
        assert isinstance(exc.timestamp, datetime)
        assert str(exc) == message

    def test_to_dict_returns_expected_structure(self):
        exc = BaseAppException("Test", 403)
        result = exc.to_dict()

        assert isinstance(result, dict)
        assert result["error"] == "Test"
        assert result["status_code"] == 403
        assert "timestamp" in result

    def test_log_error_calls_logger_with_correct_data(self):
        logger = MagicMock()
        exception = BaseAppException("Log this", status_code=422, details={"reason": "invalid format"})
        additional_context = {
            "user_id": "abc123",
            "ip_address": "127.0.0.1"
        }
        exception.log_error(logger, additional_context)
        logger.log.assert_called_once()
        level_logged = logger.log.call_args[0][0]
        log_message = logger.log.call_args[0][1]
        log_context = logger.log.call_args[1]["extra"]
        
        assert level_logged == exception.log_level
        assert "Log this" in log_message
        assert log_context["exception_type"] == "BaseAppException"
        assert log_context["error_message"] == "Log this"
        assert log_context["status_code"] == 422
        assert log_context["details"] == {"reason": "invalid format"}
        assert log_context["user_id"] == "abc123"
        assert log_context["ip_address"] == "127.0.0.1"