import json
import uuid
import os
import shortuuid

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired
from Api import *
from Api.models import Movie, MovieSchema, Users, UsersSchema
from Api.utils import save_img
import requests
import imdb
from flask_cors import CORS, cross_origin

r = requests.request("GET", "https://api.themoviedb.org/3/movie/550?api_key=03fe919b123d0ced4b33dd633638527a")

# creating instance of IMDb
ia = imdb.IMDb()

api = Blueprint('api', __name__)
CHUNK_SIZE = 512


upload = Blueprint('upload', __name__)


class Movies_(FlaskForm):
    movie = FileField('Video', validators=[FileAllowed(['mp4', 'webm', 'hd'])])
    name = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit ')


@upload.route('/upload', methods=['GET', 'POST'])
def upload_movie():
    # data = request.get_json()
    form = Movies_()
    id = ''
    if form.validate_on_submit():
        name = str(form.name.data)
        search = ia.search_movie(name)
        for i in range(0, 1):
            # getting the id
            id = search[i].movieID
        movie = requests.get(
            f"https://api.themoviedb.org/3/movie/tt{id}?api_key=03fe919b123d0ced4b33dd633638527a&language=en-US"
        )
        CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
        KEY = '03fe919b123d0ced4b33dd633638527a'

        url = CONFIG_PATTERN.format(key=KEY)
        r = requests.get(url)
        config = r.json()
        base_url = config['images']['base_url']
        sizes = config['images']['poster_sizes']

        def size_str_to_int(x):
            return float("inf") if x == 'original' else int(x[1:])

        filename = ''
        max_size = max(sizes, key=size_str_to_int)

        IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
        r = requests.get(IMG_PATTERN.format(key=KEY, imdbid=f'tt{id}'))
        api_response = r.json()

        posters = api_response['posters']
        poster_urls = []
        for poster in posters:
            rel_path = poster['file_path']
            url = "{0}{1}{2}".format(base_url, max_size, rel_path)
            poster_urls.append(url)
        for nr, url in enumerate(poster_urls):
            r = requests.get(url)
            filetype = r.headers['content-type'].split('/')[-1]
            filename = 'poster_{0}.{1}'.format(nr + 1, filetype)
        with open(os.path.join(os.path.abspath('Api/static/movies/'), filename), 'wb') as w:
            w.write(r.content)
        movie_detail = movie.text
        dict_movie = json.loads(movie_detail)
        movie_name = save_img(form.movie.data)
        video_file = request.files['movie']
        description = str(dict_movie['overview'])
        review = str(dict_movie["vote_average"])
        movies = Movie()
        movies.public_id = str(uuid.uuid4())
        movies.name = str(dict_movie['original_title'])
        movies.description = description
        movies.review = review
        movies.poster = filename
        movies.movies = movie_name
        movies.movie_data = video_file.read(CHUNK_SIZE)
        db.session.add(movies)
        db.session.commit()
    c = Movie.query.all()
    return render_template('_.html', form=form, c=c)

@upload.route('/movie/<string:u_id>', methods=['GET', 'POST'])
@login_required
def movie_show(u_id):
    movie= Movie.query.filter_by(public_id=u_id).first()
    return render_template('movie.html', movie=movie)