from flask_restful import Resource, request
from library import db
from library.utils.validators import validate_api


class AuthorList(Resource):
    def get(self):
        return db.author.get_all()

    @validate_api("author")
    def post(self):
        author_id = db.author.new(request.json['first_name'], request.json['last_name'])
        return author_id, 201


class Author(Resource):
    def get(self, author_id):
        return db.author.get(author_id) or {}, 404

    @validate_api("author")
    def put(self, author_id):
        if db.author.update(author_id, request.json['first_name'], request.json['last_name']):
            return {}, 204
        return {}, 404

    @validate_api()
    def delete(self, author_id):
        if db.author.delete(author_id):
            return {}, 204
        return {}, 404
