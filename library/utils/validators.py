from functools import wraps
from flask import request, Request, url_for
from flasgger import validate
from library.utils.constants import SWAGGER_FILE_PATH

def validate_api(schema_name=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if schema_name:
                validate(request.json, schema_name, SWAGGER_FILE_PATH)
            return fn(*args, **kwargs)
        return wrapper
    return decorator

