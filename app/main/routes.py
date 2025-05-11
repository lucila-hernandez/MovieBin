from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.main.forms import CreateMovieForm
from app.models import Movie
from app.extensions import app, bcrypt, db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/watchlist')
@login_required
def watchlist():
    return render_template('watchlist.html') 

@main.route('/create_movie', methods=['GET', 'POST'])
@login_required
def create_movie():
    form = CreateMovieForm()

    if form.validate_on_submit():
        new_movie = Movie(
            title = form.title.data,
            release_year = form.release_year.data,
            genre = form.genre.data,
            director = form.director.data
        )
        db.session.add(new_movie)
        db.session.commit()

        flash('New movie has been created sucessfully 🍿')
        return redirect(url_for('main.movie_detail', movie_id=new_movie.id))
    return render_template('create_movie.html', form=form)