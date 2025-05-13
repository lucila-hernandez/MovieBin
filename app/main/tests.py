import os
from unittest import TestCase
from datetime import date

from app.extensions import app, db, bcrypt
from app.models import User, Movie, UserMovie
from app.auth.routes import auth
from app.main.routes import main

app.register_blueprint(auth)
app.register_blueprint(main)

# Helpers
def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

def login(client):
    return client.post('/login', data={
        'username': 'me1',
        'password': 'password'
    }, follow_redirects=True)

def create_movie():
    movie = Movie(
        title="Happy Feet",
        release_year=2006,
        genre="Animation, Music",
        director="George Miller",
        photo_url="https://example.com/poster.jpg"
    )
    db.session.add(movie)
    db.session.commit()
    return movie

# Tests
class MainTests(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

    def test_homepage_logged_out(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Start by signing up or logging in', response.get_data(as_text=True))

    def test_create_movie_logged_in(self):
        with app.app_context():
            create_user()
        login(self.app)
        post_data = {
            'title': 'Happy Feet',
            'release_year': 2006,
            'genre': 'Animation',
            'director': 'George Miller',
            'photo_url': 'https://example.com/poster.jpg'
        }
        response = self.app.post('/create_movie', data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Happy Feet', response.get_data(as_text=True))

    def test_movie_detail_view(self):
        with app.app_context():
            create_user()
            movie = create_movie()
            movie_id = movie.id  
        login(self.app)
        response = self.app.get(f'/movie/{movie_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Happy Feet', response.get_data(as_text=True))

    def test_movie_log_access_requires_login(self):
        response = self.app.get('/movie_log')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fmovie_log', response.location)
