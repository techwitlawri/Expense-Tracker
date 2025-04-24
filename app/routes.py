#  Route for homepage/ dashboard

# app/routes.py

from flask import Blueprint, redirect, url_for
from flask_login import current_user

# Blueprint for main (root) routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Home page:
    - If the user is logged in, send them to the dashboard.
    - Otherwise, redirect to the login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('expenses.dashboard'))
    return redirect(url_for('auth.login'))
