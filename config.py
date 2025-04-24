#  Configuration setting

# config.py

import os

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications for performance
