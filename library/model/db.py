from .author import Author
from .book import Book
from .user import User

class Database:
    def __init__(self, pool):
        self.author = Author(pool)
        self.book = Book(pool)
        self.user = User(pool)
