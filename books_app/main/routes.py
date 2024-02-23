"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from books_app.models import Book, Author, Genre, User
from books_app.main.forms import BookForm, AuthorForm, GenreForm, UserForm

# Import app and db from events_app package so that we can run app
from books_app.extensions import app, bcrypt, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route("/")
def homepage():
    all_books = Book.query.all()
    all_users = User.query.all()
    return render_template("home.html", all_books=all_books, all_users=all_users)


@main.route("/create_book", methods=["GET", "POST"])
@login_required
def create_book():
    form = BookForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            publish_date=form.publish_date.data,
            author=form.author.data,
            audience=form.audience.data,
            genres=form.genres.data,
        )
        db.session.add(new_book)
        db.session.commit()

        flash("New book was created successfully.")
        return redirect(url_for("main.book_detail", book_id=new_book.id))
    return render_template("create_book.html", form=form)


@main.route("/create_author", methods=["GET", "POST"])
@login_required
def create_author():
    # new form
    form = AuthorForm()

    # check if valid
    if form.validate_on_submit():
        new_author = Author(
            name=form.name.data,
            biography=form.biography.data,
        )
        # add to database
        db.session.add(new_author)
        db.session.commit()

        flash("New Author was created successfully.")
        return redirect(url_for("main.homepage"))

    return render_template("create_author.html", form=form)


@main.route("/create_genre", methods=["GET", "POST"])
@login_required
def create_genre():
    # new form
    form = GenreForm()

    # check if valid
    if form.validate_on_submit():
        new_genre = Genre(name=form.name.data)
        # add to database
        db.session.add(new_genre)
        db.session.commit()

        flash("New genre was created successfully.")
        return redirect(url_for("main.homepage"))

    return render_template("create_genre.html", form=form)


@main.route("/book/<book_id>", methods=["GET", "POST"])
def book_detail(book_id):
    book = Book.query.get(book_id)
    form = BookForm(obj=book)

    # check if valid
    if form.validate_on_submit():
        # update values
        book.title = form.title.data
        book.publish_date = form.publish_date.data
        book.author = form.author.data
        book.audience = form.audience.data
        book.genres = form.genres.data

        db.session.commit()

        flash("Book updated successfully.")
        return redirect(url_for("main.book_detail", book_id=book.id))

    # check if book in user's favorites
    favorited = current_user in book.users_who_favorited

    return render_template(
        "book_detail.html",
        book=book,
        form=form,
        favorited=favorited,
    )


@main.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    user = User.query.filter_by(username=username).one()
    form = UserForm(obj=user)

    # check if valid
    if form.validate_on_submit():
        # update values
        user.username = form.username.data
        user.favorite_books = form.books.data

        db.session.commit()

        flash("User updated successfully.")
        return redirect(url_for("main.profile", username=user.username))

    return render_template("profile.html", user=user, form=form)


@main.route("/favorite/<book_id>", methods=["POST"])
@login_required
def favorite_book(book_id):
    book = Book.query.get(book_id)
    if current_user not in book.users_who_favorited:
        current_user.favorite_books.append(book)
        db.session.commit()
        flash("Book added to favorites successfully.")
    return redirect(url_for("main.book_detail", book_id=book.id))


@main.route("/unfavorite/<book_id>", methods=["POST"])
@login_required
def unfavorite_book(book_id):
    book = Book.query.get(book_id)
    if current_user in book.users_who_favorited:
        current_user.favorite_books.remove(book)
        db.session.commit()
        flash("Book removed from favorites successfully.")
    return redirect(url_for("main.book_detail", book_id=book.id))
