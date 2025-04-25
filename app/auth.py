# app/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from .extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError



# Blueprint setup
auth_bp = Blueprint('auth', __name__)

# Tell Flask-Login how to reload a user from the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Country to Currency mapping
COUNTRY_TO_CURRENCY = {
    'Nigeria': 'NGN',
    'United States': 'USD',
    'United Kingdom': 'GBP',
    'Eurozone': 'EUR',
    # Add more countries and their respective currencies here
}

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        country = request.form.get('country')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Form validation
        if not all([fullname, username, country, password, confirm_password]):
            flash('All fields are required.', 'error')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))

        try:
            # Hash the password
            hashed_password = generate_password_hash(password)
            password_hash = hashed_password

            # Create user
            new_user = User(
                fullname=fullname,
                username=username,
                country=country,
                currency = COUNTRY_TO_CURRENCY.get(country, 'USD'),
 # Optional: map country to currency
                password_hash=hashed_password
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Registration successful!', 'success')
            return redirect(url_for('expenses.dashboard'))

        except IntegrityError:
            db.session.rollback()
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET:  Show the login form.
    POST: Authenticate and log the user in.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Find the user
        user = User.query.filter_by(username=username).first()

        # Check credentials
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))

    # If GET, just render the login form
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Log the user out and redirect to login page.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
