ERROR_MESSAGES = {
    # Errores de usuario
    'USER_NOT_FOUND': "User with {field} = '{value}' not found",
    'USER_EXISTS': "User with {field} '{value}' already exists",
    'USER_INVALID_DATA_UPDATE': "No fields to update for {field}: {value}",
    
    # Errores de query_params
    'MISSING_PARAMETER': "Missing query parameter. You must provide one of: {params}",
    'TOO_MANY_PARAMETERS': "Too many parameters. Only one is allowed: {params}",
    'INVALID_PARAMETER': "Invalid parameter '{param}'. Allowed: {params}",
    
    # Errores de request body
    'MISSING_JSON_BODY': "Missing JSON body",
    'MISSING_JSON_BODY_DETAIL': "You must provide a valid JSON body in the request",
    'INVALID_JSON_FORMAT': "Invalid JSON format",
    'VALUE_CANT_BE_NULL': "Some fields cannot be null",
    'SCHEMA_VALIDATION_ERROR': "Request data validation failed",
    'FIELD_VALIDATION_ERROR': "Field '{field}' validation failed: {message}",
    
    # Errores HTTP
    'NOT_FOUND': "The requested resource was not found",
    'NOT_FOUND_ENDPOINT': "No endpoint matches '{method} {path}'",
    'METHOD_NOT_ALLOWED': "Method '{method}' is not allowed for this endpoint",
    'INTERNAL_SERVER_ERROR': "An unexpected error occurred. Please try again later.",
    'UNEXPECTED_ERROR': "An unexpected error occurred. Please contact support if this persists.",
    
    # Errores de autenticación/autorización
    'UNAUTHORIZED': "Authentication required",
    'FORBIDDEN': "Access denied",
    'TOKEN_EXPIRED': "Authentication token has expired",
    'INVALID_CREDENTIALS': "Invalid username or password",
    
    # Errores de request body
    'INVALID_JSON': "Invalid JSON format in request body",
    'MISSING_REQUIRED_FIELD': "Missing required field: {field}",
    'INVALID_FIELD_TYPE': "Field '{field}' must be of type {expected_type}",
    
    # Errores generales
    'UNKNOWN_ERROR': "Unknown error occurred"
}

def get_error_message(key: str, **kwargs) -> str:
    template = ERROR_MESSAGES.get(key, ERROR_MESSAGES['UNKNOWN_ERROR'])
    try:
        return template.format(**kwargs)
    except KeyError as e:
        return f"Error message template missing parameter: {e}"

def get_validation_message(field: str, error_type: str, **kwargs) -> str:
    error_key_map = {
        'required': 'MISSING_REQUIRED_FIELD',
        'type': 'INVALID_FIELD_TYPE',
        'max_length': 'FIELD_TOO_LONG',
        'min_length': 'FIELD_TOO_SHORT'
    }
    key = error_key_map.get(error_type, 'VALIDATION_ERROR')
    return get_error_message(key, field=field, **kwargs)
