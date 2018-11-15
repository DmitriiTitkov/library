from flask import request
from flask_restful import Resource
from library import db, swagger
from flasgger import validate, swag_from


class BookList(Resource):
    def get(self, user=""):
        books = db.book.get_all_books()
        return books

    def post(self, *args, **kwargs):
        validate(request.json, "book", "/home/dmitrii/code/library_SQL/library/book.yaml")
        print(request.json)


