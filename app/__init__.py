from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_type=None):
    app = Flask(__name__)

    if config_type == None:
        config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")

    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)

    return app


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models.User import User


def register_blueprints(app):
    from .auth import auth

    app.register_blueprint(auth, url_prefix="/")
