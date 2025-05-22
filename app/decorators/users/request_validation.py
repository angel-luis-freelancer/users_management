from functools import wraps
from flask import request, jsonify
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
                errors = []
                for error in e.errors():
                    error_info = {
                        "field": ".".join(str(loc) for loc in error["loc"]),
                        "message": error["msg"],
                        "type": error["type"]
                    }
                    errors.append(error_info)
                
                return jsonify({
                    "error": "Validation Error",
                    "details": errors
                }), 400
        return wrapper
    return decorator