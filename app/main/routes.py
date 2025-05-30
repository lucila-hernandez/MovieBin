from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.main.forms import CreateMovieForm, UserMovieForm
from app.models import Movie, UserMovie
from app.extensions import app, bcrypt, db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Render the home page"""
    return render_template('home.html')

@main.route('/movie_log')
@login_required
def movie_log():
    """Render the current user's movie log."""
    movies = Movie.query.all()  
    return render_template('movie_log.html', movies=movies)

@main.route('/create_movie', methods=['GET', 'POST'])
@login_required
def create_movie():
    """
    Display the create movie form and handle form submission.
    If the form is valid, save the new movie to the database.
    Flash a success message, and redirect to the movie detail page.
    """
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

@main.route('/delete_movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    """
    Delete a movie and its associated user tracking data.
    Removes the Movie entry and any related UserMovie records from the database.
    Redirects the user back to their movie log with a success message.
    """
    movie = Movie.query.get(movie_id)
    UserMovie.query.filter_by(movie_id=movie.id).delete()
    db.session.delete(movie)
    db.session.commit()

    flash('Movie deleted successfully 🎬')
    return redirect(url_for('main.movie_log'))

@main.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def movie_detail(movie_id):
    """
    Display movie detail page. 
    Allows the user to edit movie info and save their personal rating and watched date.
    Handles two forms, one for movie info and one for user tracking data.    
    """
    movie = Movie.query.get(movie_id)
    form = CreateMovieForm(obj=movie)
    form.submit.label.text = "Update Movie"

    user_movie = UserMovie.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()
    if not user_movie:
        user_movie = UserMovie(user_id=current_user.id, movie_id=movie.id)
        db.session.add(user_movie)
        db.session.commit()

    user_form = UserMovieForm(obj=user_movie)

    # Handle Update Movie form
    if "movie_submit" in request.form and form.validate_on_submit():
        movie.title = form.title.data
        movie.release_year = form.release_year.data
        movie.genre = form.genre.data
        movie.director = form.director.data
        movie.photo_url = form.photo_url.data
        db.session.commit()
        flash("Movie updated successfully! 🎬")
        return redirect(url_for('main.movie_detail', movie_id=movie.id))

    # Handle Save Tracking Info form
    if "rating_submit" in request.form and user_form.validate_on_submit():
        user_movie.rating = int(user_form.rating.data)
        user_movie.watched_date = user_form.watched_date.data
        db.session.commit()
        flash("Your movie rating has been updated ⭐")
        return redirect(url_for('main.movie_detail', movie_id=movie.id))

    return render_template("movie_detail.html", movie=movie, form=form, user_form=user_form)
