from flask import request
from functools import wraps
from pydantic import ValidationError

from ...exceptions import MissingJSONBodyException, InvalidJSONFormatException, SchemaValidationException

def validate_body(schema_class):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json_data = request.get_json(silent=True)
            if json_data is None:
                if request.data:
                    raise InvalidJSONFormatException()
                else:
                    raise MissingJSONBodyException()
            try:
                validated_data = schema_class(**request.get_json())
                request.validated_data = validated_data
                return f(*args, **kwargs)
            except ValidationError as e:
                raise SchemaValidationException(e.errors(), schema_class.__name__)

        return wrapper
    return decorator