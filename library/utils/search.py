from flask import Flask, current_app, _app_ctx_stack
from elasticsearch import Elasticsearch


class LibElastic:
    def __init__(self, app: Flask=None):
        self.app = app
        self.elasticsearch_options = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app, **kwargs):
        app.config.setdefault("ELASTICSEARCH_URL", 'localhost:9200')
        self.elasticsearch_options = kwargs
        app.teardown_appcontext(self.teardown)

    def __getattr__(self, item):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'elasticsearch'):
                if isinstance(ctx.app.config.get('ELASTICSEARCH_URL'), str):
                    hosts = [ctx.app.config.get('ELASTICSEARCH_URL')]
                elif isinstance(ctx.app.config.get('ELASTICSEARCH_URL'), list):
                    hosts = ctx.app.config.get('ELASTICSEARCH_URL')
                ctx.elasticsearch = Elasticsearch(hosts=hosts, **self.elasticsearch_options)

            return getattr(ctx.elasticsearch, item)


    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'elasticsearch'):
            ctx.elasticsearch = None


# TODO: refactor. Move to other file??
def indexGen(index, type):
    # TODO: add pagination to db and use generator as response
    from library import db
    books = db.book.get_all()
    for book in books:
        yield {
            "_index": index,
            "_type": type,
            "_id": book["book_id"],
            "book": book,
        }
