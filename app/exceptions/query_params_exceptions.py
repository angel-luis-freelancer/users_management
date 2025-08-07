import logging
from typing import Optional

from .base import BaseAppException
from ..constans import get_error_message

class QueryParamException(BaseAppException):
    """Error de validación general"""
    def __init__(self, message: str, status_code: int = 400, details: Optional[dict] = None, field: Optional[str] = None):
        if details is None:
            details = {}
        if field:
            details["field"] = field
        super().__init__(message, status_code, details, logging.WARNING)

class MissingParameterException(QueryParamException):
    """Parámetro requerido faltante"""
    def __init__(self, allowed_params: list):
        message = get_error_message('MISSING_PARAMETER', params=', '.join(allowed_params))
        details = {"allowed_parameters": allowed_params}
        super().__init__(message, 400, details)

class TooManyParametersException(QueryParamException):
    """Demasiados parámetros"""
    def __init__(self, allowed_params: list):
        message = get_error_message('TOO_MANY_PARAMETERS', params=', '.join(allowed_params))
        details = {"allowed_parameters": allowed_params}
        super().__init__(message, 400, details)

class InvalidParameterException(QueryParamException):
    """Parámetro inválido"""
    def __init__(self, param: str, allowed_params: list):
        message = get_error_message('INVALID_PARAMETER', param=param, params=', '.join(allowed_params))
        details = {"invalid_parameter": param, "allowed_parameters": allowed_params}
        super().__init__(message, 400, details)