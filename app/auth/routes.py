from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, bcrypt

from app.models import User, Movie, UserMovie
from app.auth.forms import SignupForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles both GET and POST for the sign up page. 
    Hashes the password with bcrypt for security.
    Saves the new user in the database. 
    Redirects to login after signup. 
    Shows flash message confirming success.
    """
    form = SignupForm()  
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles both GET and POST for the login page.
    Verifies the username and password against the database using bcrypt.
    If credentials are valid, logs the user in and redirects to the next page or homepage.
    Displays a flash message for success or failure.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash("Logged in successfully.")
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.home'))
        else:
            flash("Invalid username or password.")

    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """
    Logs the current user out and redirects to the homepage.
    Displays a flash message confirming logout.
    """
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.home'))
