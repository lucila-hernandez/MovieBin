from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, bcrypt

from app.models import User, Movie, WatchStatus, UserMovie
from app.auth.forms import SignupForm

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles both GET and POST for the sign up page. Hashes the password with bcrypt for security.
    Saves the new user in the database. Redirects to login after signup. Shows flash message confirming success.
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
