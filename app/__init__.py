# app/__init__.py
from flask import Flask
from .extensions import db, login_manager
from .auth import auth_bp
from .expenses import exp_bp  # Only import once
from dotenv import load_dotenv
from .models import User
import os

def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder='../templates')
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # ✅ Only once
    app.register_blueprint(exp_bp, url_prefix='/expenses')  # ✅ Use a prefix

    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Currency symbols made available to templates
    SYMBOLS = {
        'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥',
        'AUD': 'A$', 'CAD': 'C$', 'NGN': '₦'
    }
    app.jinja_env.globals['currency_symbol'] = lambda code: SYMBOLS.get(code, code)

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'

    with app.app_context():
        db.create_all()

    return app
