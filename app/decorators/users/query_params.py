from flask import request
from functools import wraps

from ...exceptions import MissingParameterException, TooManyParametersException, InvalidParameterException

def validate_user_query_params(allowed_params):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            params = request.args.to_dict()

            if not params:
                raise MissingParameterException(allowed_params)   

            if len(params) > 1:
                raise TooManyParametersException(allowed_params)

            key = next(iter(params))
            if key not in allowed_params:
                raise InvalidParameterException(key, allowed_params)
            value = params[key]
            return f(*args, **kwargs, query_key=key, query_value=value)
        return wrapper
    return decorator