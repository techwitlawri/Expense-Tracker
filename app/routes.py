#  Route for homepage/ dashboard

# app/routes.py

from flask import Blueprint,request, redirect, url_for, render_template,flash
from flask_login import current_user, login_required
from .extensions import db
from .models import Expense
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

@main_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = current_user  # Get the current logged-in user
    expenses = Expense.query.filter_by(user_id=user.id).all()  # Fetch user's expenses
    return render_template('dashboard.html', user=user, expenses=expenses)
@main_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'NGN']
    if request.method == 'POST':
        chosen = request.form.get('currency')
        if chosen in currencies:
            current_user.currency = chosen
            db.session.commit()
            flash('Currency updated!', 'success')
        else:
            flash('Invalid currency selection.', 'danger')
        return redirect(url_for('main.settings'))
    return render_template('settings.html', currencies=currencies)

