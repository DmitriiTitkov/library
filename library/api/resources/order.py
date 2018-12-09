import psycopg2
from flask_restful import Resource, request
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION, UNIQUE_VIOLATION

from library import db
from library.utils.validators import validate_api


class OrderList(Resource):
    def get(self, user_id=None):
        return db.order.get_all()

    @validate_api('order')
    def post(self, user_id):
        try:
            order_id = db.order.new(user_id, request.json['inventory_id'], request.json['return_date'])
            return order_id, 201
        except psycopg2.IntegrityError as e:
            if e.pgcode == FOREIGN_KEY_VIOLATION:
                # if user constraint violated return 404 because user id is part uf the url
                if e.diag.constraint_name == 'orders_user_id_fkey':
                    return {}, 404
                if e.diag.constraint_name == 'orders_inventory_fkey':
                    return {"error": "Inventory with id {} does not exist".format(request.json['inventory_id'])}, 400
            if e.pgcode == UNIQUE_VIOLATION:
                if e.diag.constraint_name == 'orders_inventory_key':
                    return {"error": "Inventory with id {} is already ordered".format(request.json['inventory_id'])}, 400
            raise


class Order(Resource):
    def get(self, order_id, user_id=None):
        return db.order.get(order_id) or {}, 404

    @validate_api('order')
    def put(self, order_id, user_id=None):
        try:
            if db.order.update(order_id, user_id, request.json['inventory_id'], request.json['return_date']):
                return {}, 204
            return {}, 404
        except psycopg2.IntegrityError as e:
            if e.pgcode == FOREIGN_KEY_VIOLATION:
                # if user constraint violated return 404 because user id is part uf the url
                if e.diag.constraint_name == 'orders_user_id_fkey':
                    return {}, 404
                if e.diag.constraint_name == 'orders_inventory_fkey':
                    return {"error": "Inventory with id {} does not exist".format(request.json['inventory_id'])}, 400
            if e.pgcode == UNIQUE_VIOLATION:
                if e.diag.constraint_name == 'orders_inventory_key':
                    return {"error": "Inventory with id {} is already ordered".format(request.json['inventory_id'])}, 400
            raise

    def delete(self, order_id, user_id=None):
        if db.order.delete(order_id):
            return {}, 204
        return {}, 404



