from .author import Author


class Database:
    def __init__(self, pool):
        self.author = Author(pool)
