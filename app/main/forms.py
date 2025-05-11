from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User


class CreateMovieForm(FlaskForm):
    """Defines the inputs that will be on the signup form and how they are validated."""
    title = StringField('Movie Title:', validators=[DataRequired(), Length(min=1, max=200)])
    release_year = IntegerField('Release Year:')
    genre = StringField('Movie Genre:', validators=[DataRequired(), Length(min=1, max=200)])
    director = StringField('Movie Director:', validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField("Add Movie")  

