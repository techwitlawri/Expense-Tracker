# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()  # Initialize the database
login_manager = LoginManager()  # Initialize login manager
