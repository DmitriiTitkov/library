from flask import Blueprint
from flask_restful import Api

from library.api.resources.book import Book, BookList
from library.api.resources.user import UserList, User
from library.api.resources.author import Author, AuthorList
from library.api.resources.order import Order, OrderList
from library.api.resources.publisher import Publisher, PublisherList

print(__name__)
api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

# register flask-restful resources
api.add_resource(BookList, "/book")
api.add_resource(Book, "/book/<book_id>")
api.add_resource(UserList, "/user")
api.add_resource(User, "/user/<user_id>")
api.add_resource(OrderList, "/order", "/user/<user_id>/order")
api.add_resource(Order, "/order/<order_id>", "/user/<user_id>/order/<order_id>")
api.add_resource(AuthorList, "/author")
api.add_resource(Author, "/author/<author_id>")
api.add_resource(PublisherList, "/publisher")
api.add_resource(Publisher, "/publisher/<publisher_id>")