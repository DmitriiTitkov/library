from flask_restful import Resource, request
from library import db
from flasgger import validate

from library.utils.validators import validate_api


class OrderList(Resource):
    def get(self, user_id=None):
        return db.order.get_all()

    @validate_api('order')
    def post(self, user_id):
        order_id = db.order.new(user_id, request.json['inventory_id'], request.json['return_date'])
        return order_id, 201


class Order(Resource):
    def get(self, order_id, user_id=None):
        return db.order.get(order_id) or {}, 404

    @validate_api('order')
    def put(self, order_id, user_id=None):
        if db.order.update(order_id, user_id, request.json['inventory_id'],
                               request.json['return_date']):
            return {}, 204
        return {}, 404

    def delete(self, order_id, user_id=None):
        if db.order.delete(order_id):
            return {}, 204
        return {}, 404
