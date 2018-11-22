from flask_restful import Resource, request
from library import db
from flasgger import validate


class AuthorList(Resource):
    def get(self):
        authors = db.author.get_all()
        return authors

    def post(self):
        validate(request.json, "author", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.author.new(request.json['title'], request.json['page_number'], request.json['author_id'],
                                   request.json['publisher_id'])


class Author(Resource):
    def get(self, author_id):
        return db.author.get(author_id)

    def put(self, author_id):
        validate(request.json, "author", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.author.update(author_id, request.json['first_name'], request.json['last_name'])

    def delete(self, author_id):
        return db.author.delete(author_id)