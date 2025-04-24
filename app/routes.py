#  Route for homepage/ dashboard

# app/routes.py

from flask import Blueprint, redirect, url_for
from flask_login import current_user
# app/routes.py

from flask import Blueprint, redirect, url_for
from flask_login import current_user

# A Blueprint for “main” (the home page and catch-all)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Home page:
    - If the user is logged in, go to their dashboard.
    - Otherwise, send them to the login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('expenses.dashboard'))
    return redirect(url_for('auth.login'))
# in app/routes.py, below your index()
@main_bp.route('/hello')
def hello():
    return "👋 Hello world!"
