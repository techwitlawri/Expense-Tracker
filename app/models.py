#  for the database model (user, Expense)

from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    """
    User model for authentication.
    Inherits UserMixin to integrate with Flask-Login.
    """
    __tablename__ = 'users'  # Optional: explicitly set table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        # For debugging: show username when printing a User object
        return f"<User {self.username}>"


class Expense(db.Model):
    """
    Expense model to track individual expenses.
    Each expense belongs to one user (foreign key).
    """
    __tablename__ = 'expenses'  # Optional: explicitly set table name

    id          = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount      = db.Column(db.Float, nullable=False)
    date        = db.Column(db.DateTime, default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


     # Foreign key linking this expense to a User

    def __repr__(self):
        # For debugging: show description and amount
        return f"<Expense {self.description} - ${self.amount}>"