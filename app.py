import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager


# from resources.item import blp as ItemBlueprint
# from resources.store import blp as StoreBlueprint
from resources.instructor import blp as Instructor_Blueprint
from resources.course import blp as Course_Blueprint
from resources.tag import blp as Tag_Blueprint
from resources.user import blp as User_Blueprint
from db import db


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Course Rating REST API"
    app.config["API_VERSION"] = "v1"



    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"



    # add SQLalchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    app.config["JWT_SECRET_KEY"] = "jose"
    jwt = JWTManager(app)

    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     if identity == 1:
    #         return {"is_admin": True}
    #     return {"is_admin": False}
    #
    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header, jwt_payload):
    #     return (
    #         jsonify(({"message": "The token has expired.",
    #                   "error": "token expired"})),
    #         401,
    #     )
    #
    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return (
    #         jsonify({
    #             "message": "Signature verification failed",
    #             "error": "invalid token"
    #         }),
    #         401,
    #     )
    #
    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     return (
    #         jsonify(
    #             {
    #                 "description": "Request does not contain an access token.",
    #                 "error": "authorization_required",
    #             }
    #         ),
    #         401,
    #     )
    # when app is created tell SQLALCHEMY to create all database tables
    with app.app_context():
        db.create_all()

    api = Api(app)
    api.register_blueprint(Instructor_Blueprint)
    api.register_blueprint(Course_Blueprint)
    api.register_blueprint(Tag_Blueprint)
    api.register_blueprint(User_Blueprint)
    return app