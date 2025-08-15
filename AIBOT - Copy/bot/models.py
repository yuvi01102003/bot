from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now() )
    userip = db.Column(db.String(10000))
    aiop = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(30), unique=True)
    phone = db.Column(db.Integer())
    password = db.Column(db.String(100))
    otp = db.Column(db.String(6), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    chats = db.relationship('Chats')

