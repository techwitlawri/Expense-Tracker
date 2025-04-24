# app/models.py

from .extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(80), unique=True, nullable=False)
    password    = db.Column(db.String(200), nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

class Expense(db.Model):
    __tablename__ = 'expenses'
    id          = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount      = db.Column(db.Float, nullable=False)
    date        = db.Column(db.DateTime, default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Expense {self.description} - ${self.amount}>"
