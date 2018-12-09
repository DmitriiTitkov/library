import psycopg2
from flask_restful import Resource, request
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION, UNIQUE_VIOLATION

from library import db
from flasgger import validate

from library.api.resources import LibApiResource
from library.utils.validators import validate_api


class PublisherList(LibApiResource):
    def get(self):
        return db.publisher.get_all()

    @validate_api("publisher")
    def post(self):
        try:
            publisher_id = db.publisher.new(request.json['title'])
            return publisher_id, 201

        except psycopg2.IntegrityError as e:
            if e.pgcode == UNIQUE_VIOLATION:
                if e.diag.constraint_name == 'unique_title':
                    return {"error": "Publisher with name '{}' is already exist".format(request.json['title'])}, 400
            raise


class Publisher(LibApiResource):
    def get(self, publisher_id):
        return db.publisher.get(publisher_id) or {}, 404

    @validate_api("publisher")
    def put(self, publisher_id):
        try:
            if db.publisher.update(publisher_id, request.json['title']):
                return {}, 204
            return {}, 404
        except psycopg2.IntegrityError as e:
            if e.pgcode == UNIQUE_VIOLATION:
                if e.diag.constraint_name == 'unique_title':
                    return {"error": "Publisher with name '{}' is already exist".format(request.json['title'])}, 400
            raise

    def delete(self, publisher_id):
        if db.publisher.delete(publisher_id):
            return {}, 204
        return {}, 404


if True:
    print("True")
else:
    print("False")
