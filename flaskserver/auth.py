import os
import traceback

import bcrypt
import jwt
from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

from . import db
from .models import Account, AccountRoles

auth = Blueprint("auth", __name__)

@auth.route("/isAdmin", methods=["POST"])
def check_admin():
    accountid = request.json.get("userID", None)
    accountrole = AccountRoles.query.filter_by(accountid=accountid).first()

    if not accountrole or accountrole.roleid != 1:
        response = {"isAdmin": False}
    else:
        response = {"isAdmin": True}
    
    return response
    

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


@auth.route("/verify", methods=["GET"])
@jwt_required()
def verify_token():
    return "valid token", 200


@auth.route("/register", methods=["POST"])
def register():
    registerDict = request.get_json()

    newAccount = Account(
        email=registerDict["email"],
        passwordhash=hash_password(registerDict["password"]),
        accountname=registerDict["username"],
    )
    db.session.add(newAccount)
    db.session.commit()
    response = {"registered": "true"}
    return response, 200


@auth.route("/getUser", methods=["POST"])
@jwt_required()
def get_user():
    userID = request.json.get("userID", None)

    account = Account.query.filter_by(id=userID).first()
    if not account:
        return str(401)
    response = jsonify(account.as_dict())
    return response


## these methods should work for the hashing
def hash_password(password):
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def check_password(hashed_password, user_password):
    password_bytes = user_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, bytes.fromhex(hashed_password[2:]))
