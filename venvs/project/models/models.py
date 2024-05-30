import os
from project import db, login_manager, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Bungalow(db.Model):

    __tablename__ = 'bungalows'

    id = db.Column(db.Integer,primary_key=True)
    naam = db.Column(db.Text)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id', name="type_id"))  # ForeignKey naar Type
    type = db.Relationship('Type', backref='bungalow', uselist="False")

    def __init__(self, naam, type_id):
        self.naam = naam
        self.type_id = type_id

class Type(db.Model):

    __tablename__ = 'types'

    id = db.Column(db.Integer,primary_key=True)
    grootte = db.Column(db.Integer)
    weekprijs = db.Column(db.Integer)

    def __init__(self, grootte, weekprijs):
        self.grootte = grootte
        self.weekprijs = weekprijs

class Boeking(db.Model):

    __tablename__ = 'boekingen'
    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id', name="user_id"))
    bungalowId = db.Column(db.Integer, db.ForeignKey('bungalows.id', name="bungalow_id"))
    weekNr = db.Column(db.Integer)

    def __init__(self, userId, bungalowId, weekNr):
        self.userId = userId
        self.bungalowId = bungalowId
        self.weekNr = weekNr

class User(db.Model, UserMixin):

    __tablename__ = 'users'
     
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)