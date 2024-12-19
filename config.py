import os
from dotenv import load_dotenv

project_folder = os.path.expanduser("")
load_dotenv(os.path.join(project_folder, ".env"))

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DB_TYPE = os.getenv("DB_TYPE")
DB_TYPE = os.getenv("DB_TYPE")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


class Config(object):
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", default="BAD_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = (
        f"{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret"


class ProductionConfig(Config):
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(object):
    TESTING = True
    SECRET_KEY = os.getenv("SECRET_KEY", default="BAD_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}"
    )
