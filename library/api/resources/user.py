import psycopg2
from flask import request
from flask_restful import Resource
from psycopg2.errorcodes import UNIQUE_VIOLATION

from library import db
from library.utils.validators import validate_api


class UserList(Resource):
    # TODO: Add Authentication for all endpoints

    def get(self):
        return db.user.get_all()

    @validate_api('user')
    def post(self):
        try:
            user_id = db.user.new(request.json['firstName'], request.json['lastName'], request.json['username'],
                                  request.json['password'], request.json['email'].lower())
            return user_id, 201
        except psycopg2.IntegrityError as e:
            if e.pgcode == UNIQUE_VIOLATION:
                if e.diag.constraint_name == 'unique_email':
                    return {"error": "User with email '{}' is already exist".format(request.json['email'])}, 400
            raise


class User(Resource):
    def get(self, user_id):
        return db.user.get(user_id) or {}, 404

    @validate_api('user')
    def put(self, user_id):
        try:
            if db.user.update(user_id, request.json['firstName'], request.json['lastName'], request.json['username'],
                              request.json['password'], request.json['email'].lower()):
                return {}, 204
            return "User not found", 404
        except psycopg2.IntegrityError as e:
            if e.pgcode == UNIQUE_VIOLATION:
                if e.diag.constraint_name == 'unique_email':
                    return {"error": "User with email '{}' is already exist".format(request.json['email'])}, 400
            raise

    def delete(self, user_id):
        if db.user.delete(user_id):
            return {}, 204
        return "", 404
