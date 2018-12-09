from functools import wraps
from flask import request
from flasgger import validate
from flask import current_app

def validate_api(schema_name=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if schema_name:
                validate(request.json, schema_name, current_app.config.get('SWAGGER', {}).get('SWAGGER_FILE_PATH'))
            return fn(*args, **kwargs)
        return wrapper
    return decorator

