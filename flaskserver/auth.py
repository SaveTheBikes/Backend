import os

import bcrypt
import jwt
from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import create_access_token

from . import db
from .models import Account

auth = Blueprint("auth", __name__)


##todo session token not expired endpoint
# TODO add access_token verify endpoint
# TODO add get_profile endpoint
def verify_token(token):
    try:
        payload = jwt.decode(token, os.getenv["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."


@auth.route("/login", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    account = Account.query.filter_by(email=email).first()
    if not account or not check_password(account.passwordhash, password):
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
        passwordhash=hash_password(registerDict["password"]),
        accountname=registerDict["username"],
    )
    db.session.add(newAccount)
    db.session.commit()
    response = {"registered": "true"}
    return response, 200


## this method is an example of how to check if your token isn't expired


@auth.route("/protected")
def protected():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token is missing!"}), 403

    verification_result = verify_token(token)
    if isinstance(verification_result, str):
        return jsonify({"message": verification_result}), 403

    # Token is valid
    return jsonify({"message": "Access granted", "data": verification_result})


## these methods should work for the hashing
def hash_password(password):
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def check_password(hashed_password, user_password):
    password_bytes = user_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, bytes.fromhex(hashed_password[2:]))
