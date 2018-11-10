from flasgger import Swagger
from flask import Flask
from library.api.api import api_blueprint
from library .html import html_blueprint
import json
from psycopg2.pool import ThreadedConnectionPool
from library.model.db import Database


app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Library API',
    'uiversion': 3
}
Swagger(app, template_file='openapi.yaml')

app.register_blueprint(api_blueprint, url_prefix="/api")
app.register_blueprint(html_blueprint, url_prefix="/")

config: dict = json.load(open('library/config.json'))
db_config = config["database"]


pool = ThreadedConnectionPool(1, 20,
                              database=db_config["database_name"],
                              user=db_config["user"],
                              password=db_config["password"],
                              host=db_config["host"],
                              port=db_config["port"])

db = Database(pool)
print(db.author.get_all_authors())


