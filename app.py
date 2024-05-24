import os

from flask import Flask, jsonify
from flask_smorest import Api
from sqlalchemy.exc import SQLAlchemyError

import models
from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint


def create_app(db_url=None):

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.__init__(app)

    api = Api(app)

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(e):
        error_message = str(e)
        response = jsonify(
            {
                "code": 500,
                "status": "Internal Server Error",
                "message": f"An error occurred creating the store: {error_message}",
            }
        )
        response.status_code = 500
        return response

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app


# http://localhost:5000/swagger-ui
