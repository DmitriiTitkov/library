from flask import request
from flask_restful import Resource
from library import db
from flasgger import validate


class BookList(Resource):
    def get(self, user=""):
        books = db.book.get_all_books()
        return books

    def post(self):
        validate(request.json, "book", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.book.create_book(request.json['title'], request.json['page_number'], request.json['author_id'],
                                   request.json['publisher_id'])
