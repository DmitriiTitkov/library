from flask import request
from flask_restful import Resource
from library import db


class UserList(Resource):
    # TODO: Add Validation and Authentication for all endpoints

    def get(self):
        users = db.user.get_all()
        return users

    def post(self):

        # validate(request.json, "user", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        # return db.book.new(request.json['title'], request.json['page_number'], request.json['author_id'],
        #                            request.json['publisher_id'])
        return db.user.new(request.json['firstName'], request.json['lastName'])


class User(Resource):
    def get(self, user_id):
        return db.user.get(user_id)

    def put(self, user_id):
        # validate(request.json, "book", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.user.update(user_id, request.json['firstName'], request.json['lastName'])

    def delete(self, user_id):
        return db.user.delete(user_id)