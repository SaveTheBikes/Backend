from flask import Flask, Blueprint
from dataclasses import dataclass
from . import db 

models = Blueprint('models', __name__)

class DictEnabled:
    __abstract__ = True

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Account(db.Model, DictEnabled):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key = True)
    accountname = db.Column(db.String())
    email = db.Column(db.String())
    passwordhash = db.Column(db.String())

    def __init__(self, accountname, email, passwordhash):
        self.accountname = accountname
        self.email = email
        self.passwordhash = passwordhash
    
    def __repr__(self):
        return '<account name {}> & <email {}> & <id {}>'.format(self.accountname, self.email, self.id)

class AccountBikePost(db.Model):
    __tablename__ = "accountbikeposts"

    accountid = db.Column(db.Integer, primary_key = True)
    postid = db.Column(db.Integer, primary_key = True)

    def __init__(self, accountid, postid):
        self.accountid = accountid
        self.postid = postid

class BikePostLocation(db.Model):
    __tablename__ = "bikepostlocation"

    address = db.Column(db.String())
    dateseen = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key = True)

    locationlat = db.Column(db.Float)
    locationlon = db.Column(db.Float)
    postid = db.Column(db.Integer)

    def __init__(self, address, dateseen, locationlat, locationlon, postid):
        self.address = address
        self.dateseen = dateseen
        self.locationlat = locationlat
        self.locationlon = locationlon
        self.postid = postid

class BikePost(db.Model, DictEnabled):
    __tablename__ = "bikepost"

    id = db.Column(db.Integer, primary_key = True)
    datestolen = db.Column(db.DateTime)
    title = db.Column(db.String())
    # b64 encoding
    picture = db.Column(db.UnicodeText)
    colour = db.Column(db.String())
    model = db.Column(db.String())

    def __init__(self, datestolen, title, picture, colour, model):
        self.datestolen = datestolen
        self.title = title
        self.picture = picture
        self.colour = colour
        self.model = model
    
    def __repr__(self):
        return '<datestolen {}> & <title {}>'.format(self.datestolen, self.title)
