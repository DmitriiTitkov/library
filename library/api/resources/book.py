from flask_restful import Resource, reqparse, request
from library import db
from flasgger import validate

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted', location="path")
parser.add_argument('name')
# args = parser.parse_args()


class Book(Resource):
    def get(self, book_id):
        return db.book.get_book(book_id)

    def put(self, book_id):
        validate(request.json, "book", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.book.update_book(book_id, request.json['title'], request.json['page_number'], request.json['author_id'],
                                   request.json['publisher_id'])

    def delete(self, book_id):
        return db.book.delete_book(book_id)