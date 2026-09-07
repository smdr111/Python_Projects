from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os
import requests


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db.init_app(app)


# CREATE TABLE
class Movies(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer,nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float,nullable=True)
    ranking: Mapped[int] = mapped_column(Integer,nullable=True)
    review:  Mapped[str] = mapped_column(String(250),nullable=True)
    img_url: Mapped[str] = mapped_column(String(250),nullable=False)
with app.app_context():
    db.create_all()


# CREATE RATING FORM
class RateMovieForm(FlaskForm):
    new_rating = StringField('Your Rating Out of 10 e.g. 7.5',validators=[DataRequired()])
    new_review = StringField('Your Review',validators=[DataRequired()])
    submit = SubmitField(label='Done')


# CREATE RATING FORM
class AddMovieForm(FlaskForm):
    movie_title = StringField('Movie Title',validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')


@app.route("/")
def home():
    result = db.session.execute(db.select(Movies).order_by(Movies.rating))
    all_movies = result.scalars().all()
    n = len(all_movies)
    for indx in range(n):
        all_movies[indx].ranking = n - indx
    db.session.commit()
    return render_template("index.html",movies=all_movies)


@app.route('/add',methods=['POST','GET'])
def add():
    add_form = AddMovieForm()
    if add_form.validate_on_submit():
        url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.getenv('MOVIE_DB_ACCESS_TOKEN')}"
        }
        mv_title = add_form.movie_title.data
        response = requests.get(url, params={"query":mv_title}, headers=headers)
        data = response.json()
        return render_template('select.html',movies=data['results'])
    return render_template('add.html',form=add_form)


@app.route('/add_new')
def add_new():
    movie_id = request.args.get('id')
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('MOVIE_DB_ACCESS_TOKEN')}"
    }
    data = requests.get(url, headers=headers).json()
    movie = db.session.execute(db.select(Movies).where(Movies.title == data['title'])).scalar()
    if not movie:
        new_movie = Movies(
            title=data['title'],
            year=int(data['release_date'][:4]) if data.get('release_date') else 0,
            description=data['overview'],
            img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}",
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('edit',id=new_movie.id))
    return redirect(url_for('home'))


@app.route('/edit',methods=['POST','GET'])
def edit():
    rating_form = RateMovieForm()
    movie_id = request.args.get('id')
    if rating_form.validate_on_submit():
        # UPDATE RECORD
        movie_to_update = db.get_or_404(Movies, movie_id)
        movie_to_update.rating = float(rating_form.new_rating.data)
        movie_to_update.review = rating_form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))
    movie = db.get_or_404(Movies, movie_id)
    return render_template("edit.html", form=rating_form,movie=movie)


@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movies, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
