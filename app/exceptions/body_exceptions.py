import logging

from typing import List, Dict, Any

from ..constans import get_error_message
from .base import BaseAppException

class MissingJSONBodyException(BaseAppException):
    """Body JSON faltante"""
    def __init__(self):
        message = get_error_message('MISSING_JSON_BODY')
        details = {
            "message": get_error_message('MISSING_JSON_BODY_DETAIL'),
            "expected": "Valid JSON body"
        }
        super().__init__(message, 400, details, logging.WARNING)

class InvalidJSONFormatException(BaseAppException):
    """Formato JSON inválido"""
    def __init__(self, error_detail: str = None):
        message = get_error_message('INVALID_JSON_FORMAT')
        details = {
            "parse_error": error_detail,
            "expected": "Valid JSON format"
        }
        super().__init__(message, 400, details, logging.WARNING)


class InvalidNullValueExeption(BaseAppException):
    """Alguien campo no puede ser nulo"""
    def __init__(self, null_fields: List[str] = None, allowed_fields: List[str] = None):
        message = {
            "parse_error": get_error_message('VALUE_CANT_BE_NULL'),
            "expected": f"fields_cant_be_null: {allowed_fields or []}"
        }
        details = message
        super().__init__(message, 400, details, logging.WARNING)


class SchemaValidationException(BaseAppException):
    """Error de validación de schema (Pydantic)"""
    def __init__(self, validation_errors: List[Dict[str, Any]], schema_name: str = ""):
        message = get_error_message('SCHEMA_VALIDATION_ERROR')
        processed_errors = []
        for error in validation_errors:
            field_path = ".".join(str(loc) for loc in error.get("loc", []))
            processed_error = {
                "field": field_path,
                "message": error.get("msg", "Unknown validation error"),
                "type": error.get("type", "unknown"),
                "input": error.get("input", None)
            }
            processed_errors.append(processed_error)
            
        details = {
            "validation_errors": processed_errors,
            "schema": schema_name,
            "error_count": len(processed_errors)
        }
        super().__init__(message, 400, details, logging.WARNING)
    
    def to_dict(self) -> Dict[str, Any]:
        """Override para incluir formato específico para errores de validación"""
        base_dict = super().to_dict()
        base_dict["validation_errors"] = self.details.get("validation_errors", [])
        return base_dict