

import pytest
from app import create_app, db
from app.models import User
from datetime import datetime, UTC
from werkzeug.security import generate_password_hash

# Fixture to provide a test client and setup database

@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

# Test user registration
def test_user_registration(test_client):
    response = test_client.post('/auth/register', data={
        'fullname': 'Test User',
        'username': 'testuser',
        'country': 'Nigeria',  # ensure this matches your COUNTRY_TO_CURRENCY keys
        'password': 'testpass',
        'confirm_password': 'testpass'
    }, follow_redirects=True)

    print(response.data)  # for debugging

    assert b'Registration successful!' in response.data

    # Verify user was added
    with create_app().app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.fullname == 'Test User'

# Test user login
def test_user_login(test_client):
    # Create user directly in DB
    with create_app().app_context():
        user = User(
            fullname='Test User',
            username='testuser',
            country='Nigeria',
            currency='NGN',
            created_at=datetime.now(UTC)
        )
        user.password_hash = generate_password_hash('testpass')
        db.session.add(user)
        db.session.commit()

    # Test login
    response = test_client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)

    print(response.data)  #  for debugging

    assert b'Logged in successfully!' in response.data


def test_user_logout(test_client):
    # Register and log in user
    test_client.post('/auth/register', data={
        'fullname': 'Test User',
        'username': 'testlogout',
        'country': 'Nigeria',
        'password': 'logoutpass',
        'confirm_password': 'logoutpass'
    }, follow_redirects=True)

    # Logout
    response = test_client.get('/auth/logout', follow_redirects=True)

    assert b'You have been logged out.' in response.data

def test_invalid_login(test_client):
    # Attempt to log in with wrong credentials
    response = test_client.post('/auth/login', data={
        'username': 'nonexistent',
        'password': 'wrongpass'
    }, follow_redirects=True)

    assert b'Invalid username or password.' in response.data

def test_protected_route_requires_login(test_client):
    # Try to access dashboard without logging in
    response = test_client.get('/expenses/dashboard', follow_redirects=True)

    # Should be redirected to login
    assert b'Login' in response.data or b'Please log in to access this page' in response.data


def test_duplicate_registration(test_client):
    # Register once
    test_client.post('/auth/register', data={
        'fullname': 'Test User',
        'username': 'duplicateuser',
        'country': 'Nigeria',
        'password': 'testpass',
        'confirm_password': 'testpass'
    }, follow_redirects=True)

    # Try to register with same username
    response = test_client.post('/auth/register', data={
        'fullname': 'Test User Two',
        'username': 'duplicateuser',
        'country': 'Nigeria',
        'password': 'testpass',
        'confirm_password': 'testpass'
    }, follow_redirects=True)

    assert b'Username already exists.' in response.data

