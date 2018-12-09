from flasgger import Swagger
from flask import Flask

from library.database.db import Database
from library.utils.search import LibElastic


db = Database()
es = LibElastic()


def create_app(config='config.json'):
    app = Flask(__name__)
    app.config.from_json(config)

    # Registering blueprints

    from library.api.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    from library.html import html_blueprint
    app.register_blueprint(html_blueprint, url_prefix="/")

    # ADD EXTENSIONS
    es.init_app(app)

    # TODO: check flasgger app factory pattern
    _ = Swagger(app, template_file=app.config.get("SWAGGER", {}).get("SWAGGER_FILE_PATH"))

    db.init_app(app)
    return app
