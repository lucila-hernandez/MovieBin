from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User


class SignupForm(FlaskForm):
    """Defines the inputs that will be on the form and how to validate them"""
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose another one.')