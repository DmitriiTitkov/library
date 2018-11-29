from flask_restful import Resource, request
from library import db
from flasgger import validate

from library.utils.validators import validate_api


class PublisherList(Resource):
    def get(self):
        return db.publisher.get_all()

    @validate_api("publisher")
    def post(self):
        publisher_id = db.publisher.new(request.json['title'])
        return publisher_id, 201

class Publisher(Resource):
    def get(self, publisher_id):
        return db.publisher.get(publisher_id) or {}, 404

    @validate_api("publisher")
    def put(self, publisher_id):
        if db.publisher.update(publisher_id, request.json['title']):
            return {}, 204
        return {}, 404

    def delete(self, publisher_id):
        if db.publisher.delete(publisher_id):
            return {}, 204
        return {}, 404