from library.database.models.author import Author
from library.database.models.book import Book
from library.database.models.order import Order
from library.database.models.publisher import Publisher
from library.database.models.user import User


class Database:
    def __init__(self, pool):
        self.author = Author(pool)
        self.book = Book(pool)
        self.order = Order(pool)
        self.publisher = Publisher(pool)
        self.user = User(pool)


