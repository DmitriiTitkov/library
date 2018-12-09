from flask import Blueprint
from flask_restful import Api

from library.api.resources.book import Book, BookList
from library.api.resources.search import Search
from library.api.resources.user import UserList, User
from library.api.resources.author import Author, AuthorList
from library.api.resources.order import Order, OrderList
from library.api.resources.publisher import Publisher, PublisherList
from library.api.resources.inventory import Inventory, InventoryList

print(__name__)
api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)

# register flask-restful resources
api.add_resource(BookList, "/book")
api.add_resource(Book, "/book/<int:book_id>")
api.add_resource(UserList, "/user")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(OrderList, "/order", "/user/<int:user_id>/order")
api.add_resource(Order, "/order/<int:order_id>", "/user/<user_id>/order/<int:order_id>")
api.add_resource(AuthorList, "/author")
api.add_resource(Author, "/author/<int:author_id>")
api.add_resource(PublisherList, "/publisher")
api.add_resource(Publisher, "/publisher/<int:publisher_id>")
api.add_resource(InventoryList, "/inventory")
api.add_resource(Inventory, "/inventory/<int:inventory_id>")

api.add_resource(Search, "/search")