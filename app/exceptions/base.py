import logging

from datetime import datetime
from typing import Dict, Any, Optional

class BaseAppException(Exception):
    """Excepción base para toda la aplicación"""
    def __init__(self, 
            message: str, 
            status_code: int = 500, 
            details: Optional[Dict[str, Any]] = None, 
            log_level: int = logging.ERROR):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.log_level = log_level
        self.timestamp = datetime.utcnow()
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la excepción a diccionario para respuesta JSON"""
        return {
            "error": self.message,
            "timestamp": self.timestamp.isoformat(),
            "status_code": self.status_code
        }
    
    def log_error(self, logger: logging.Logger, additional_context: Optional[Dict] = None):
        """Registra el error en los logs"""
        context = {
            "exception_type": self.__class__.__name__,
            "error_message": self.message,
            "status_code": self.status_code,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }
        if additional_context:
            safe_context = {k: v for k, v in additional_context.items() 
                if k not in [
                    'message', 
                    'msg', 
                    'args', 
                    'levelname', 
                    'levelno', 
                    'pathname', 
                    'filename', 
                    'module', 
                    'lineno', 
                    'funcName', 
                    'created', 
                    'msecs', 
                    'relativeCreated', 
                    'thread', 
                    'threadName', 
                    'processName', 
                    'process', 
                    'name'
                ]
            }
            context.update(safe_context)
        logger.log(self.log_level, f"Application Error: {self.message}", extra=context)