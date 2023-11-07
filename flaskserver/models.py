from flask import Flask, Blueprint
from dataclasses import dataclass
from . import db 

models = Blueprint('models', __name__)

class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key = True)
    accountname = db.Column(db.String())
    email = db.Column(db.String())
    passwordhash = db.Column(db.String())

    def __init__(self, accountname, email, passwordhash):
        self.id = id
        self.accountname = accountname
        self.email = email
        self.passwordhash = passwordhash
    
    def __repr__(self):
        return '<account name {}> & <email {}> & <id {}>'.format(self.accountname, self.email, self.id)