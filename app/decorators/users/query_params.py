from functools import wraps
from flask import request, jsonify

def validate_user_query_params(allowed_params):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            params = request.args.to_dict()

            if not params:
                return jsonify({
                    "error": f"Missing query parameter. You must provide one of: {', '.join(allowed_params)}"
                }), 400

            if len(params) > 1:
                return jsonify({
                    "error": f"Too many parameters. Only one is allowed: {', '.join(allowed_params)}"
                }), 400

            key = next(iter(params))
            if key not in allowed_params:
                return jsonify({
                    "error": f"Invalid parameter '{key}'. Allowed: {', '.join(allowed_params)}"
                }), 400

            value = params[key]
            return f(*args, **kwargs, query_key=key, query_value=value)
        return wrapper
    return decorator