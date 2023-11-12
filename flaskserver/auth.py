from flask import Blueprint, Flask, request
from flask_jwt_extended import create_access_token

from . import db
from .models import Account

import bcrypt

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    account = Account.query.filter_by(email=email).first()
    if not account or account.passwordhash != password:
        return str(401)
    print("Logged in user with account: {}".format(account.id))
    access_token = create_access_token(identity=email)
    response = {"access_token": access_token}
    return response


@auth.route("/register", methods=["POST"])
def register():
    registerDict = request.get_json()

    ## todo passwords must be hashed.
    newAccount = Account(
        email=registerDict["email"],
        passwordhash=registerDict["password"],
        accountname=registerDict["username"],
    )
    db.session.add(newAccount)
    db.session.commit()
    response = {"registered": "true"}
    return response, 200

## these methods should work for the hashing, however they are not being used yet.

def hash_password(password):
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

def check_password(hashed_password, user_password):
    password_bytes = user_password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hashed_password)

