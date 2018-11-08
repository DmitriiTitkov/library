from flask import Blueprint
from flask_restful import Api
from .resources.book import Book

print(__name__)
api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

# register flask-restful resources
api.add_resource(Book, "/book/")

