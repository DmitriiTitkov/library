from psycopg2.pool import ThreadedConnectionPool

from library.database.models.author import Author
from library.database.models.book import Book
from library.database.models.order import Order
from library.database.models.publisher import Publisher
from library.database.models.user import User
from library.database.models.inventory import Inventory


class Database:
    def __init__(self, app=None):
        self.app = app
        if app and pool:
            self.init_app(app, pool)

    def init_app(self, app):
        try:
            db_config = app.config.get("DATABASE")
            pool = self._create_connection_pool(**db_config)

        except KeyError:
            raise Exception("Database configuration is incorrect")

        self.author = Author(pool)
        self.book = Book(pool)
        self.order = Order(pool)
        self.publisher = Publisher(pool)
        self.user = User(pool)
        self.inventory = Inventory(pool)


    def _create_connection_pool(self, database_name, user, password, host, port):
        return ThreadedConnectionPool(1, 20,
                                      database=database_name,
                                      user=user,
                                      password=password,
                                      host=host,
                                      port=port)


