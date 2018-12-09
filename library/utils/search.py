from library import db
from elasticsearch import Elasticsearch


class LibElastic:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        pass

    def connect:
        Elasticsearch('http://localhost:9200')


def indexGen(index, type):
    # TODO: add pagination to db and use generator as response
    books = db.book.get_all()
    for book in books:
        yield {
            "_index": index,
            "_type": type,
            "_id": book["book_id"],
            "book": book,
        }
