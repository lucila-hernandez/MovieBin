import os
from unittest import TestCase
from datetime import date

from app.extensions import app, db, bcrypt
from app.models import User, Movie, UserMovie
from app.auth.routes import auth
from app.main.routes import main

app.register_blueprint(auth)
app.register_blueprint(main)

# Helper
def create_user():
    """Creates a test user with username 'me1' and password 'password'."""
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

# Tests
class AuthTests(TestCase):
    """
    Tests for MovieBin authentication routes (/signup, /login, /logout).
    Verifies user creation, session handling, and error feedback.
    """
    def setUp(self):
        """Set up a fresh database and test client before each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

    def test_signup(self):
        """Test that a new user can successfully sign up."""
        post_data = {
            'username': 'new_user',
            'password': 'securepassword'
        }
        self.app.post('/signup', data=post_data, follow_redirects=True)

        with app.app_context():
            user = User.query.filter_by(username='new_user').first()
            self.assertIsNotNone(user)

    def test_login_correct_password(self):
        """Test that a user can log in with the correct password."""
        with app.app_context():
            create_user()

        post_data = {
            'username': 'me1', 
            'password': 'password'
        }
        response = self.app.post('/login', data=post_data, follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn('Logout', response_text)

    def test_login_nonexistent_user(self):
        """Test that logging in with a nonexistent user shows an error message."""
        post_data = {
            'username': 'ghost', 
            'password': 'nope'
        }
        response = self.app.post('/login', data=post_data, follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn('Invalid username or password.', response_text)

    def test_logout(self):
        """Test that a logged-in user can log out sucessfully."""
        with app.app_context():
            create_user()

        self.app.post('/login', data={'username': 'me1', 'password': 'password'}, follow_redirects=True)
        self.app.get('/logout', follow_redirects=True)

        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)
