from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, ValidationError, URL
from app.models import User

class CreateMovieForm(FlaskForm):
    """Defines the inputs that will be on the signup form and how they are validated."""
    title = StringField('Movie Title:', validators=[DataRequired(), Length(min=1, max=200)])
    release_year = IntegerField('Release Year:')
    genre = StringField('Movie Genre:', validators=[DataRequired(), Length(min=1, max=200)])
    director = StringField('Movie Director(s):', validators=[DataRequired(), Length(min=1, max=200)])
    photo_url = StringField(
        'Movie Photo URL:',
        validators=[
            DataRequired(),
            URL(message="Must be a valid URL"),
            Length(max=1000)
        ]
    )
    submit = SubmitField("Add Movie")  

class UserMovieForm(FlaskForm):
    """Form for tracking user's relationship with a movie."""
    rating = SelectField(
        'Rating',
        choices=[
            ('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'),
            ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')
        ],
        validators=[DataRequired()]
    )
    watched_date = DateField('Watched Date', validators=[DataRequired()])
    submit = SubmitField('Save Tracking Info')