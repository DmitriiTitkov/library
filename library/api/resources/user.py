from flask import request
from flask_restful import Resource
from library import db
from library.utils.validators import validate_api


class UserList(Resource):
    # TODO: Add Validation and Authentication for all endpoints

    def get(self):
        return db.user.get_all()

    @validate_api('user')
    def post(self):
        user_id = db.user.new(request.json['firstName'], request.json['lastName'], request.json['username'],
                              request.json['password'], request.json['email'].lower())
        return user_id, 201


class User(Resource):
    def get(self, user_id):
        return db.user.get(user_id) or {}, 404

    @validate_api('user')
    def put(self, user_id):
        if db.user.update(user_id, request.json['firstName'], request.json['lastName'], request.json['username'],
                          request.json['password'], request.json['email'].lower()):
            return {}, 204
        return "User not found", 404

    def delete(self, user_id):
        if db.user.delete(user_id):
            return {}, 204
        return "", 404
