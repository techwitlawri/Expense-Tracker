# app/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from .models import User
from .extensions import db, login_manager

# Blueprint setup
auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# Tell Flask-Login how to reload a user from the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET:  Show the registration form.
    POST: Validate and create a new user, then redirect to login.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Basic validation
        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('auth.register'))

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose another.', 'error')
            return redirect(url_for('auth.register'))

        # Hash the password and save the new user
        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    # If GET, just render the registration form
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
        if user and bcrypt.check_password_hash(user.password, password):
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
