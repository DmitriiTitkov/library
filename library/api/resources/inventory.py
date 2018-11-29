from datetime import datetime

from flask_restful import Resource, request
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
        inventory_id = db.inventory.new(request.json['book_id'], request.json['publisher_id'], request.json['isbn'],
                                        request.json['page_number'], request.json['edition'],
                                        datetime(int(request.json['year_published']), 1, 1, 0),
                                        request.json['amount'], )
        return inventory_id, 201


class Inventory(Resource):
    def get(self, inventory_id):
        return db.inventory.get(inventory_id) or {}, 404


    @validate_api('inventory')
    def put(self, inventory_id):
        if db.inventory.update(inventory_id, request.json['book_id'], request.json['publisher_id'],
                                   request.json['isbn'], request.json['page_number'], request.json['edition'],
                                   datetime(int(request.json['year_published']), 1, 1, 0)):
            return {}, 204
        return {}, 404

    def delete(self, inventory_id):
        if db.inventory.delete(inventory_id):
            return {}, 204
        return {}, 404
