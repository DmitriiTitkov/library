from flasgger import Swagger
from flask import Flask, g


import json
from psycopg2.pool import ThreadedConnectionPool
from library.database.db import Database

config: dict = json.load(open('library/config.json'))
db_config = config["database"]
pool = ThreadedConnectionPool(1, 20,
                              database=db_config["database_name"],
                              user=db_config["user"],
                              password=db_config["password"],
                              host=db_config["host"],
                              port=db_config["port"])

db = Database(pool)
app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Library API',
    'uiversion': 3
}
# TODO validation for all parameters. NOw only request body is validated
swagger = Swagger(app, template_file='openapi.yaml')
# print(swagger.get_schema('book'))

def create_app():
    # Registering blueprints

    from library.api.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    from library.html import html_blueprint
    app.register_blueprint(html_blueprint, url_prefix="/")

    return app
