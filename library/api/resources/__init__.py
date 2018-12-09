from functools import wraps
from flask_restful import Resource
import re

re.compile("\(\)=\(\)")

def db_error_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # TODO: Common database error handler for future use.
            raise
    return wrapper


class LibApiResource(Resource):
    method_decorators = {'post': [db_error_handler], 'put': [db_error_handler], }