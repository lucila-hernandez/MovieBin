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
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

# Tests
class AuthTests(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

    def test_signup(self):
        post_data = {
            'username': 'new_user',
            'password': 'securepassword'
        }
        self.app.post('/signup', data=post_data, follow_redirects=True)

        with app.app_context():
            user = User.query.filter_by(username='new_user').first()
            self.assertIsNotNone(user)

    def test_login_correct_password(self):
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
        post_data = {
            'username': 'ghost', 
            'password': 'nope'
        }
        response = self.app.post('/login', data=post_data, follow_redirects=True)
        response_text = response.get_data(as_text=True)
        self.assertIn('Invalid username or password.', response_text)

    def test_logout(self):
        with app.app_context():
            create_user()

        self.app.post('/login', data={'username': 'me1', 'password': 'password'}, follow_redirects=True)
        self.app.get('/logout', follow_redirects=True)

        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)
