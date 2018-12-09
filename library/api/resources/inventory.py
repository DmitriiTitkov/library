from datetime import datetime

import psycopg2
from flask_restful import Resource, request
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION

from library import db
from flasgger import validate
from library.utils.validators import validate_api


# TODO: Add error handler for db Integrity errors.


class InventoryList(Resource):
    @validate_api()
    def get(self):
        return db.inventory.get_all()

    @validate_api('inventory')
    def post(self):
        try:
            inventory_id = db.inventory.new(request.json['book_id'], request.json['publisher_id'], request.json['isbn'],
                                            request.json['page_number'], request.json['edition'],
                                            datetime(int(request.json['year_published']), 1, 1, 0),
                                            request.json['amount'], )
            return inventory_id, 201
        except psycopg2.IntegrityError as e:
            if e.pgcode == FOREIGN_KEY_VIOLATION:
                if e.diag.constraint_name == 'inventory_publisher_fkey':
                    return {"error": "Publisher with id {} does not exist".format(request.json['publisher_id'])}, 400
                elif e.diag.constraint_name == 'inventory_book_fkey':
                    return {"error": "Book with id {} does not exist".format(request.json['book_id'])}, 400
            raise

class Inventory(Resource):
    def get(self, inventory_id):
        return db.inventory.get(inventory_id) or {}, 404

    @validate_api('inventory')
    def put(self, inventory_id):
        try:
            if db.inventory.update(inventory_id, request.json['book_id'], request.json['publisher_id'],
                                       request.json['isbn'], request.json['page_number'], request.json['edition'],
                                       datetime(int(request.json['year_published']), 1, 1, 0)):
                return {}, 204
            return {}, 404

        except psycopg2.IntegrityError as e:
            if e.pgcode == FOREIGN_KEY_VIOLATION:
                if e.diag.constraint_name == 'inventory_publisher_fkey':
                    return {"error": "Publisher with id {} does not exist".format(request.json['publisher_id'])}, 400
                elif e.diag.constraint_name == 'inventory_book_fkey':
                    return {"error": "Book with id {} does not exist".format(request.json['book_id'])}, 400
            raise



    def delete(self, inventory_id):
        if db.inventory.delete(inventory_id):
            return {}, 204
        return {}, 404
