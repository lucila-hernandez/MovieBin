from .extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class User(db.Model):
    id = 
    username =
    password =

class Movie(db.Model):
    id =
    title = 
    release_year =
    genre =
    director =
    notes =

class User_Movie(db.Model):
    id =
    user_id =
    movie_id = 
    status = 
    rating = 
    watched = 