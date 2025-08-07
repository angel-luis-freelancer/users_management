import logging

from .base import BaseAppException
from ..constans import get_error_message

class UserNotFoundException(BaseAppException):
    """Usuario no encontrado"""
    def __init__(self, field: str, value: str):
        message = get_error_message('USER_NOT_FOUND', field=field, value=value)
        details = {"search_key": field, "search_value": value}
        super().__init__(message, 404, details, logging.WARNING)

class UserAlreadyExistsException(BaseAppException):
    """Usuario ya existe"""
    def __init__(self, field: str, value: str):
        message = get_error_message('USER_EXISTS', field=field, value=value)
        details = {"conflict_field": field, "conflict_value": value}
        super().__init__(message, 409, details, logging.WARNING)

class InvalidUserDataException(BaseAppException):
    """Datos de usuario inválidos"""
    def __init__(self, field: str, value: str = "Invalid data"):
        message = get_error_message('USER_INVALID_DATA_UPDATE', field=field, value=value)
        details = {"invalid_field": field, "reason": value}
        super().__init__(message, 400, details, logging.WARNING)