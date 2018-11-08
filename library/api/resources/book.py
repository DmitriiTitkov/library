from flask_restful import Resource


class Book(Resource):
    def get(self):
        return "This is the book"

    def post(self):
        pass