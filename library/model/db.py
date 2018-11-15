from .author import Author
from .book import Book


class Database:
    def __init__(self, pool):
        self.author = Author(pool)
        self.book = Book(pool)
