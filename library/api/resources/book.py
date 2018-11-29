from flask_restful import Resource, request
from library import db
from library.api.resources import LibApiResource
from library.utils.validators import validate_api


class BookList(LibApiResource):
    def get(self):
        return db.book.get_all()

    @validate_api("book")
    def post(self):
        book_id = db.book.new(request.json['title'],  request.json['author_id'])
        return book_id, 201


class Book(LibApiResource):
    def get(self, book_id):
        return db.book.get(book_id) or {}, 404

    @validate_api("book")
    def put(self, book_id):
        if db.book.update(book_id, request.json['title'], request.json['author_id']):
            return {}, 204
        return {}, 404

    def delete(self, book_id):
        if db.book.delete(book_id):
            return {}, 204
        return {}, 404
