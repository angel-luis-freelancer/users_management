import logging
from typing import Optional

from .base import BaseAppException
from ..constans import get_error_message

class DatabaseException(BaseAppException):
    """Error de base de datos general"""
    def __init__(self, original_error: Optional[str] = None):
        details = {"original_error": str(original_error).replace('"', "'")} if original_error else {}
        super().__init__(get_error_message('UNKNOWN_ERROR'), 500, details, logging.ERROR)