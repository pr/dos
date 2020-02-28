from dos.open_api import OpenAPI
from dos.flask_wrappers import wrap_validation, wrap_handler, wrap_route
from flask import Flask, redirect, jsonify, url_for, render_template

from .api.dog import get as dog_get
from .api.cat import get as cat_get


def create_app():
    app = Flask(__name__)

    open_api = OpenAPI("Pet Shop API", "1.0")

    open_api.add_contact("Pet Shop Dev Team", "https://www.example.com", "pet_shop@example.com")
    open_api.add_logo("/static/pet_shop.png", "#7D9FC3", "Pet Shop", "/")
    open_api.add_tag(
        "introduction",
        "Welcome! This is the documentation for the Pet Shop API.",
    )
    open_api.add_tag(
        "Authentication and Authorization",
        "Authentication and Authorization Information. For this basic dos example, there is none.",
    )
    open_api.add_tag(
        "dog",
        "Endpoints for interacting with a Dog",
    )
    open_api.add_tag(
        "cat",
        "Endpoints interacting with a Cat",
    )

    open_api.add_disclaimer(
        "This file is generated automatically. Do not edit it directly! Edit "
        "the input_schema and output_schema of the endpoint you are changing."
    )

    handler_mapping = [
        (dog_get, "/dog/get", "get"),
        (cat_get, "/cat/get", "get")
    ]

    for module, path, http_method in handler_mapping:
        handler = wrap_handler(module.__name__, module.handler)
        handler = wrap_validation(handler, module)
        wrap_route(app, handler, path, http_method)
        open_api.document(module, path, http_method)

    @app.route("/")
    def index():  # pylint: disable=unused-variable
        return render_template("index.html")

    @app.route("/source")
    def redirect_to_source():  # pylint: disable=unused-variable
        return redirect(url_for("open_api_endpoint"))

    @app.route("/docs")
    def docs():  # pylint: disable=unused-variable
        return render_template("docs.html")

    @app.route("/open_api.json")
    def open_api_endpoint():  # pylint: disable=unused-variable
        return jsonify(open_api)

    return app
