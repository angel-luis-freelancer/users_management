from functools import wraps
from flask import request
from werkzeug.exceptions import BadRequest
from pydantic import ValidationError

def validate_body(schema_class):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                validated_data = schema_class(**request.get_json())
                request.validated_data = validated_data  # Inyecta datos validados
                return f(*args, **kwargs)
            except ValidationError as e:
                raise BadRequest(str(e))
        return wrapper
    return decorator