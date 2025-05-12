from .extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class User(db.Model, UserMixin):
    """Represents a user with login credentials and associated movies."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    movies = db.relationship('UserMovie', backref='user', lazy=True)

class Movie(db.Model):
    """Stores basic information about a movie."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    release_year = db.Column(db.Integer)
    genre = db.Column(db.String(80))
    director = db.Column(db.String(80))
    photo_url = db.Column(db.String(1000))

    users = db.relationship('UserMovie', backref='movie', lazy=True)

class WatchStatus(enum.Enum):
    """Enum for movie watch status."""
    WATCHED = "Watched"
    PLAN_TO_WATCH = "Plan to Watch"
    IN_PROGRESS = "In Progress"

class UserMovie(db.Model):
    """Links a user to a movie with custom status, rating, and notes."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    
    rating = db.Column(db.Integer)
    watched_date = db.Column(db.Date)
