from flask import request
from flask_restful import Resource
from library import db
from flasgger import validate


class UserList(Resource):
    # TODO: Add Validation and Authentication for all endpoints

    def get(self):
        users = db.user.get_all_users()
        return users

    def post(self):

        # validate(request.json, "user", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        # return db.book.create_book(request.json['title'], request.json['page_number'], request.json['author_id'],
        #                            request.json['publisher_id'])
        return db.user.add_user(request.json['firstName'], request.json['lastName'])
