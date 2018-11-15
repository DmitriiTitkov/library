from flask import Blueprint

html_blueprint = Blueprint("html", __name__)


@html_blueprint.route('/')
def home():
    return "This is the Home Page"

