from functools import wraps

import psycopg2
from flask_restful import Resource


def db_error_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except psycopg2.IntegrityError as e:
            raise e

    return wrapper


class LibApiResource(Resource):
    method_decorators = {'post': [db_error_handler]}