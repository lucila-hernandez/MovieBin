from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.main.forms import CreateMovieForm
from app.models import Movie
from app.extensions import app, bcrypt, db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Render the home page"""
    return render_template('home.html')

@main.route('/watchlist')
@login_required
def watchlist():
    """Render the current user's movie watchlist."""
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
            director = form.director.data,
            photo_url=form.photo_url.data
        )
        db.session.add(new_movie)
        db.session.commit()

        flash('New movie has been created sucessfully 🍿')
        return redirect(url_for('main.movie_detail', movie_id=new_movie.id))
    return render_template('create_movie.html', form=form)

@main.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def movie_detail(movie_id):
    movie = Movie.query.get(movie_id)
    form = CreateMovieForm(obj=movie)

    form.submit.label.text = "Update Movie"

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.release_year = form.release_year.data
        movie.genre = form.genre.data
        movie.director = form.director.data
        movie.photo_url = form.photo_url.data
        db.session.commit()
        flash("Movie updated successfully! 🍿")
        return redirect(url_for('main.movie_detail', movie_id=movie.id))

    return render_template('movie_detail.html', movie=movie, form=form)