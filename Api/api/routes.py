import os
import uuid

from flask import Blueprint, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired

from api import db, request, render_template, json
from api.models import Movie, MovieSchema
from api.utils import save_img

api = Blueprint('api', __name__)


# this returns all the movies
@api.route('/')
def home():
    movies = Movie.query.order_by(Movie.date_uploaded.desc()).all()
    movie_schema = MovieSchema(many=True)
    result = movie_schema.dump(movies)
    # g= [i['poster'] for i in result]
    return jsonify({'d': result})




class Movies_(FlaskForm):
    movie = FileField('Video', validators=[FileAllowed(['mp4', 'webm', 'hd'])])
    photo = FileField('', validators=[FileAllowed(['jpg', 'png']), DataRequired()])
    name = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])
    review = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit ')


@api.route('/upload', methods=['GET', 'POST'])
def upload():
    # data = request.get_json()
    form = Movies_()

    if form.validate_on_submit():
        photo_file = save_img(form.photo.data)

        file = request.files['photo']
        name = form.name.data
        movie_name = save_img(form.movie.data)
        video_file = request.files['movie']
        description = form.description.data
        review = form.review.data

        movies = Movie()
        movies.public_id = str(uuid.uuid4())
        movies.name = name
        movies.description = description
        movies.review = float(review)
        movies.poster = photo_file
        movies.poster_data = file.read()
        movies.movies = movie_name
        movies.movie_data = video_file.read()
        db.session.add(movies)
        db.session.commit()

    return render_template('_.html', form=form)


@api.route('/get/movie/<string:u_id>/')
def get_by_name(u_id):
    movie_name = Movie.query.filter_by(public_id=u_id).first()
    movie_schema = MovieSchema()
    result = movie_schema.dump(movie_name)
    return jsonify({
        'name': result['name'],
        'description': result['description'],
        'review': result['review'],
        'poster': result['poster'],
        'movies': result['movies']
    })
