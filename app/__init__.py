#  Initialize app, setup extensions

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os


#  Load environment variable from .env

load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    # Create the Flask application instance
    app = Flask(__name__)

    # Set up app configuration (secret key, db URI from .env)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///expense_tracker.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # Set up where to redirect if user not logged in
    login_manager.login_view = 'auth.login'


     # Register Blueprints
    from .auth import auth_bp
    from .expenses import exp_bp
    from .routes import main_bp

    app.register_blueprint(auth_bp,  url_prefix= '')
    app.register_blueprint(exp_bp,  url_prefix= '')
    app.register_blueprint(main_bp)
    with app.app_context():
        from . import routes 

        # Create database tables for all models
        db.create_all()

    return app
