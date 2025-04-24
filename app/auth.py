# app/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask_bcrypt import Bcrypt

# Import the shared db and login_manager from your app package
from . import db, login_manager
from .models import User

# Create the Blueprint for auth routes
auth_bp = Blueprint(
    'auth',             # this blueprint’s name
    __name__,           # module where it lives
    template_folder='../templates'
)

# Initialize Bcrypt (for hashing passwords)
bcrypt = Bcrypt()

# Tell Flask-Login how to load a user from the session
@login_manager.user_loader
def load_user(user_id):
    """
    Given *user_id*, return the corresponding User object.
    Flask-Login will use this to reload the user from the session.
    """
    return User.query.get(int(user_id))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET:  Show the registration form.
    POST: Validate form data, create a new User with a hashed password, and redirect to login.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username is already taken
        if User.query.filter_by(username=username).first():
            flash('Username is already taken', 'danger')
            return redirect(url_for('auth.register'))

        # Hash the password and create the user
        pwd_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=pwd_hash)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    # GET request just renders the form
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET:  Show the login form.
    POST: Verify credentials, log the user in, and redirect to dashboard.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        # Check credentials
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('expenses.dashboard'))

        flash('Invalid username or password', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Log the current user out and redirect to the login page.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
