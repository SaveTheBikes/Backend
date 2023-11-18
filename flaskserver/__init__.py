import os
from os import path

import psycopg2
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# connect to our database
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SecretKey")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWTSecretKey")

    ## also, this will need to be manually pasted and should not enter github.
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    CORS(app)
    JWTManager(app)
    db.init_app(app)

    # register our blueprints

    from .auth import auth
    from .bikes import bikes

    CORS(auth)
    CORS(bikes)
    app.register_blueprint(auth, url_prefix="/auth/")
    app.register_blueprint(bikes, url_prefix="/bikes/")

    return app
