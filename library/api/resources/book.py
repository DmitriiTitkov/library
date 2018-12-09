import psycopg2
from flask_restful import request
from psycopg2.errorcodes import UNIQUE_VIOLATION, FOREIGN_KEY_VIOLATION

from library import db
from library.api.resources import LibApiResource
from library.utils.validators import validate_api


class BookList(LibApiResource):
    def get(self):
        return db.book.get_all()

    @validate_api("book")
    def post(self):
        try:
            book_id = db.book.new(request.json['title'],  request.json['author_id'])
            return book_id, 201
        except psycopg2.IntegrityError as e:
            if e.pgcode == FOREIGN_KEY_VIOLATION:
                return {"error": "Author with id {} does not exist".format(request.json['author_id'])}, 400


class Book(LibApiResource):
    def get(self, book_id):
        return db.book.get(book_id) or {}, 404

    @validate_api("book")
    def put(self, book_id):
        try:
            if db.book.update(book_id, request.json['title'], request.json['author_id']):
                return {}, 204
            return {}, 404
        except psycopg2.IntegrityError as e:
            if e.pgcode == FOREIGN_KEY_VIOLATION:
                return {"error": "Author with id {} does not exist".format(request.json['author_id'])}, 400


    def delete(self, book_id):
        if db.book.delete(book_id):
            return {}, 204
        return {}, 404
