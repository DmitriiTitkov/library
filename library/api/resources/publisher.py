from flask_restful import Resource, request
from library import db
from flasgger import validate


class PublisherList(Resource):
    def get(self):
        publishers = db.publisher.get_all_publishers()
        return publishers

    def post(self):
        validate(request.json, "publisher", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.publisher.new(request.json['title'])


class Publisher(Resource):
    def get(self, publisher_id):
        return db.publisher.get_publisher(publisher_id)

    def put(self, publisher_id):
        validate(request.json, "publisher", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.publisher.update(publisher_id, request.json['title'])

    def delete(self, publisher_id):
        return db.publisher.delete_publisher(publisher_id)