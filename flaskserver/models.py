from flask import Flask, Blueprint
from dataclasses import dataclass
from . import db 

models = Blueprint('models', __name__)

class DictEnabled:
    __abstract__ = True

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class AccountRoles(db.Model):
    __tablename__ = 'accountroles'

    accountid = db.Column(db.Integer, primary_key = True)
    roleid = db.Column(db.Integer, primary_key = True)

    def __init__(self, accountid, userid):
        self.accountid = accountid
        self.userid = userid

class Account(db.Model, DictEnabled):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key = True)
    accountname = db.Column(db.String())
    email = db.Column(db.String())
    passwordhash = db.Column(db.String())
    phonenumber = db.Column(db.String())

    def __init__(self, accountname, email, passwordhash, phonenumber):
        self.accountname = accountname
        self.email = email
        self.passwordhash = passwordhash
        self.phonenumber = phonenumber
    
    def __repr__(self):
        return '<account name {}> & <email {}> & <id {}>'.format(self.accountname, self.email, self.id)

class AccountBikePost(db.Model):
    __tablename__ = "accountbikeposts"

    accountid = db.Column(db.Integer, primary_key = True)
    postid = db.Column(db.Integer, primary_key = True)

    def __init__(self, accountid, postid):
        self.accountid = accountid
        self.postid = postid

class BikePost(db.Model, DictEnabled):
    __tablename__ = "bikepost"

    id = db.Column(db.Integer, primary_key = True)
    datestolen = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(), nullable=False)
    # b64 encoding
    picture = db.Column(db.UnicodeText, nullable=False)
    colour = db.Column(db.String(), nullable=False)
    model = db.Column(db.String(), nullable=False)
    locationlat = db.Column(db.Float, nullable=False)
    locationlon = db.Column(db.Float, nullable=False)

    def __init__(self, datestolen, title, picture, colour, model, locationlat, locationlon):
        self.datestolen = datestolen
        self.locationlat = locationlat
        self.locationlon = locationlon
        self.title = title
        self.picture = picture
        self.colour = colour
        self.model = model
    
    def __repr__(self):
        return '<datestolen {}> & <title {}>'.format(self.datestolen, self.title)
