from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_cors import CORS
import psycopg2

#connect to our database
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'wontBeTheKey'
    app.config["JWT_SECRET_KEY"] = "wontBeTheKey"
    
    ## also, this will need to be manually pasted and should not enter github.
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    JWTManager(app)
    db.init_app(app)

    # register our blueprints

    from .auth import auth

    CORS(auth)
    app.register_blueprint(auth, url_prefix='/auth/')

    return app
