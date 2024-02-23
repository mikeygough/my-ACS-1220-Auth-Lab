from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    DateField,
    SelectField,
    SubmitField,
    TextAreaField,
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from books_app.models import Audience, Book, Author, Genre, User
from books_app.extensions import app, db, bcrypt


class BookForm(FlaskForm):
    """Form to create a book."""

    title = StringField(
        "Book Title", validators=[DataRequired(), Length(min=3, max=80)]
    )
    publish_date = DateField("Date Published")
    author = QuerySelectField(
        "Author", query_factory=lambda: Author.query, allow_blank=False
    )
    audience = SelectField("Audience", choices=Audience.choices())
    genres = QuerySelectMultipleField("Genres", query_factory=lambda: Genre.query)
    submit = SubmitField("Submit")


class AuthorForm(FlaskForm):
    """Form to create an author."""

    name = StringField(
        "Author Name",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=80,
                message="Your author name needs to be between 1 and 80 chars.",
            ),
        ],
    )

    biography = TextAreaField(
        "Biography",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=240,
                message="Your author biography needs to be between 3 and 240 chars.",
            ),
        ],
    )
    submit = SubmitField("Submit")


class GenreForm(FlaskForm):
    """Form to create a genre."""

    name = StringField(
        "Genre Name",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=80,
                message="Your genre name needs to be between 3 and 80 chars.",
            ),
        ],
    )
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    """Form to create a user."""

    username = StringField(
        "User Name",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=80,
                message="Your username needs to be between 3 and 80 chars",
            ),
        ],
    )
    books = QuerySelectMultipleField("Books", query_factory=lambda: Book.query)
    submit = SubmitField("Submit")
