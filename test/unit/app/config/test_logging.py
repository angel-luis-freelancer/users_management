from flask import Flask
import json
import logging
import os

from app.config.logging import CustomJSONFormatter, setup_logging

class TestLogging:
    def test_custom_json_formatter_basic_log(self):
        """Testea que el formatter convierta un log básico en JSON correctamente"""
        formatter = CustomJSONFormatter()

        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )

        result = formatter.format(record)
        parsed = json.loads(result)

        assert parsed["logger"] == "test.logger"
        assert parsed["level"] == "INFO"
        assert parsed["message"] == "Test message"
        assert "timestamp" in parsed

    def test_custom_json_formatter_with_extra_fields(self):
        """Verifica que los campos extra aparezcan en el log JSON"""
        formatter = CustomJSONFormatter()

        record = logging.LogRecord(
            name="test.logger",
            level=logging.ERROR,
            pathname=__file__,
            lineno=20,
            msg="Error message",
            args=(),
            exc_info=None
        )
        # Agregar campos extra
        record.exception_type = "CustomError"
        record.error_message = "Something went wrong"
        record.status_code = 500
        record.details = {"debug": "info"}

        result = formatter.format(record)
        parsed = json.loads(result)

        assert parsed["exception_type"] == "CustomError"
        assert parsed["error_message"] == "Something went wrong"
        assert parsed["status_code"] == 500
        assert parsed["details"] == {"debug": "info"}

    def test_setup_logging_creates_log_dir(self, tmp_path):
        """Verifica que setup_logging cree la carpeta de logs y configure correctamente los loggers"""
        # Cambiar el directorio de logs temporalmente
        logs_dir = tmp_path / "logs"
        os.chdir(tmp_path)  # Simula raíz del proyecto

        app = Flask(__name__)
        setup_logging(app)

        assert logs_dir.exists()
        assert logs_dir.is_dir()

        logger = logging.getLogger("app")
        logger.info("Log de prueba")

        # Verifica que se haya creado el archivo
        log_file = logs_dir / "app.log"
        assert log_file.exists()