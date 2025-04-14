from functools import wraps
from flask import request
from werkzeug.exceptions import BadRequest

def validate_query_params(allowed_params):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            invalid_params = set(request.args.keys()) - set(allowed_params)
            if invalid_params:
                raise BadRequest(f"Parámetros permitidos: {', '.join(allowed_params)}. Inválidos: {', '.join(invalid_params)}")
            return f(*args, **kwargs)
        return wrapper
    return decorator