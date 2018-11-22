from flask_restful import Resource, request
from library import db
from flasgger import validate


class OrderList(Resource):
    def get(self, user_id=None):
        orders = db.order.get_all()
        return orders

    def post(self, user_id):
        validate(request.json, "order", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.order.new(user_id, request.json['inventory_id'], request.json['return_date'])


class Order(Resource):
    def get(self, order_id, user_id=None):
        return db.order.get(order_id)

    def put(self, order_id, user_id=None):
        validate(request.json, "order", "/home/dmitrii/code/library_SQL/library/openapi.yaml")
        return db.order.update(order_id, user_id, request.json['inventory_id'],
                               request.json['return_date'])

    def delete(self, order_id, user_id=None):
        return db.order.delete(order_id)
