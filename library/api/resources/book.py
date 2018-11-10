from flask_restful import Resource
from flasgger import swag_from


class Book(Resource):
    def get(self, user=""):
        return "This is the book \n and this is a user: {}".format(user)

    def post(self):
        pass