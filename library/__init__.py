import elasticsearch
from flasgger import Swagger
from flask import Flask, g
import json
from psycopg2.pool import ThreadedConnectionPool
from library.database.db import Database

from library.utils.search import LibElastic
from library.utils.serializer import parser


config: dict = json.load(open('library/config.json'))
db_config = config["database"]
pool = ThreadedConnectionPool(1, 20,
                              database=db_config["database_name"],
                              user=db_config["user"],
                              password=db_config["password"],
                              host=db_config["host"],
                              port=db_config["port"])

db = Database(pool)


# print(swagger.get_schema('book'))

print(parser.specification)

def create_app():
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'Library API',
        'uiversion': 3
    }
    swagger = Swagger(app, template_file='openapi.yaml')

    # Registering blueprints

    from library.api.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    from library.html import html_blueprint
    app.register_blueprint(html_blueprint, url_prefix="/")

    # ADD EXTENTIONS

    es = LibElastic(app)

    return app
