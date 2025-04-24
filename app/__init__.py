
# app/__init__.py
from flask import Flask
from .extensions import db, login_manager  # Import extensions here
from .auth import auth_bp
from .expenses import exp_bp
from dotenv import load_dotenv
from .models import User  # Import models after app setup
import os

load_dotenv()  # Load environment variables

def create_app():
    app = Flask(__name__)

    # Configure the app with settings from the Config class
    app.config.from_object('config.Config')

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Set up where to redirect if user not logged in
    login_manager.login_view = 'auth.login'

    # Register Blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(exp_bp)

    with app.app_context():
        # Create database tables for all models
        db.create_all()

    return app
