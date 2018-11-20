from flask import Blueprint
from flask_restful import Api

from library.api.resources.book import Book
from library.api.resources.booklist import BookList
from library.api.resources.userlist import UserList

print(__name__)
api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

# register flask-restful resources
api.add_resource(BookList, "/book")
api.add_resource(Book, "/book/<book_id>")
api.add_resource(UserList, "/user")

