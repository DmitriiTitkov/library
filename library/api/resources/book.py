from flask_restful import Resource, request
from library import db
from flasgger import validate


class BookList(Resource):
    def get(self):
        books = db.book.get_all()
        return books

    def post(self):
        validate(request.json, "book", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.book.new(request.json['title'], request.json['page_number'], request.json['author_id'],
                           request.json['publisher_id'])


class Book(Resource):
    def get(self, book_id):
        return db.book.get_all(book_id)

    def put(self, book_id):
        validate(request.json, "book", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.book.update(book_id, request.json['title'], request.json['page_number'], request.json['author_id'],
                              request.json['publisher_id'])

    def delete(self, book_id):
        return db.book.delete(book_id)