import json
import uuid
import os

from flask import Blueprint, render_template, request, jsonify

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired
from Api import *
from Api.models import Movie, Series, SeriesSchema, Series_Season, Series_Episodes, Series_SeasonSchema
from Api.utils import save_img
import requests
try:
    import imdb
except ImportError:
    pass
try:
    r = requests.request("GET", "https://api.themoviedb.org/3/movie/550?api_key=03fe919b123d0ced4b33dd633638527a")
except:
    pass



import cloudinary as Cloud
import cloudinary.uploader
import cloudinary.api

Cloud.config(
    cloud_name = 'du05mneox',
    api_key= '371873492641178',
    api_secret= 'MdVOWo1ZXyAO9OgLJZ1DokqPgQk'
)



# creating instance of IMDb
try:
    ia = imdb.IMDb()
except:
    pass
api = Blueprint('api', __name__)
CHUNK_SIZE = 512

upload = Blueprint('upload', __name__)


class Movies_(FlaskForm):
    movie = FileField('Video', validators=[FileAllowed(['mp4', 'webm', 'hd'])])
    name = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit ')


@upload.route('/upload/movie', methods=['GET', 'POST'])
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
        credit = requests.get(f"https://api.themoviedb.org/3/movie/tt{id}/credits?api_key={KEY}&language=en-US")
        casts = credit.text
        lists = []
        json_casts = json.loads(casts)
        cast = json_casts['cast']
        for i in cast:
            lists.append(i['original_name'])

        description = str(dict_movie['overview'])
        review = str(dict_movie["vote_average"])
        movies = Movie()
        movies.public_id = str(uuid.uuid4())
        movies.name = str(dict_movie['original_title'])
        movies.description = description
        movies.review = review
        genres = dict_movie['genres']
        movies.cast1 = lists[0]
        movies.cast2 = lists[1]
        movies.cast3 = lists[2]
        movies.cast4 = lists[3]
        genre = []
        company = dict_movie['production_companies']
        com = []
        for i in company:
            com.append(i['name'])
        for i in genres:
            genre.append(i['name'])
        movies.genre = json.loads({"data": genre})
        movies.creator = com[0]
        movies.created_on = str(dict_movie['release_date'])
        movies.runtime = str(dict_movie['runtime'])


        Cloud.uploader.upload(f"{os.path.join(os.path.abspath('Api/static/movies/'), filename)}",
                              chunk_size=6000000,
                              public_id=str(dict_movie['original_title']),
                              overwrite=True,
                              eager=[
                                  {"width": 300, "height": 300, "crop": "pad", "audio_codec": "none"},
                                  {"width": 160, "height": 100, "crop": "crop", "gravity": "south",
                                   "audio_codec": "none"}],
                              eager_async=True,
                              notification_url="https://mysite.example.com/notify_endpoint",
                              resource_type="image")


        Cloud.uploader.upload(f"{os.path.join(os.path.abspath('Api/static/movies/'), movie_name)}",
                              chunk_size=6000000,
                              public_id=str(dict_movie['original_title']),
                              overwrite=True,
                              eager=[
                                  {"width": 300, "height": 300, "crop": "pad", "audio_codec": "none"},
                                  {"width": 160, "height": 100, "crop": "crop", "gravity": "south",
                                   "audio_codec": "none"}],
                              eager_async=True,
                              notification_url="https://mysite.example.com/notify_endpoint",
                              resource_type="video")

        
        db.session.add(movies)
        db.session.commit()
    c = ''
    try:
        c = Movie.query.all()
    except:
        pass
    return render_template('_.html', form=form, c=c)



class Series_(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit ')


@upload.route('/upload/series', methods=['GET', 'POST'])
def upload_series():
    form = Series_()
    id = ''
    if form.validate_on_submit():
        name = str(form.name.data)
        search = ia.search_movie(name)
        for i in range(0, 1):
            # getting the id
            id = search[i].movieID
        # getting information
        series = ia.get_movie(id)
        title = series.data['title']
        total_seasons = series.data['number of seasons']
        runtimes = series.data['runtimes'][0]
        genre = series.data['genres']
        plot = series.data['plot outline']
        first_aired = series.data['year']
        sound_mix = series.data['sound mix'][0]
        aspect_ratio = series.data['aspect ratio']
        rating = series.data['rating']
        languages = series.data['languages']
        kind = series.data['kind']
        series_years = series.data['series years']
        series = Series()
        series.name = title
        series.sound_mix = sound_mix
        series.aspect_ratio = aspect_ratio
        series.rating = rating
        series.languages = languages
        series.kind = kind
        series.series_years = series_years
        series.overview = plot
        series.runtime = runtimes
        series.first_aired_on = first_aired
        series.public_id = str(uuid.uuid4())
        series.genre = genre
        series.total_seasons = total_seasons
        db.session.add(series)
        db.session.commit()

    c = ''
    try:
        c = Series.query.all()
    except:
        pass
    return render_template('series.html', form=form, c=c)


@upload.route('/upload/series/<string:series_name>/season', methods=['GET', 'POST'])
def upload_season(series_name):
    series_ = Series.query.filter_by(name=series_name).first()

    id = ''
    name = str(series_.name)
    search = ia.search_movie(name)
    for i in range(0, 1):
        # getting the id
        id = search[i].movieID
    # getting information
    series = ia.get_movie(id)
    episodes = series.data['seasons']
    s_ep = Series_Season(season=series_)
    for season_list in episodes:
        s_ep.season_id = int(season_list)
        db.session.add(s_ep)
        db.session.commit()
    return jsonify({

        "message": 'Added'
    })


class Episode(FlaskForm):
    movie = FileField('Video', validators=[FileAllowed(['mp4', 'webm', 'hd'])])
    number = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')


@upload.route('/upload/series/<string:series_name>/season/<string:season_id>/episode', methods=['GET', 'POST'])
def upload_episode(series_name, season_id, ep_no):
    series_ = Series.query.filter_by(name=series_name).first()
    s_season = Series_Season.query.filter_by(season=series_).filter_by(season_id=season_id).first()
    form = Episode()
    if form.validate_on_submit():
        episode_number = int(form.number.data)
        id = ''
        name = str(series_.name)
        search = ia.search_movie(name)
        for i in range(0, 1):
            # getting the id
            id = search[i].movieID
        # getting information
        series = ia.get_movie(id)
        ia.update(series, 'episodes')
        episodes = series.data['episodes']
        files = request.files['movie']
        episodes_data={}
        for episode_list in episodes.keys():
            if episode_number in episodes[episode_list].keys():
                episodes_data.update({'name':episodes[episode_list]['title'], 'no':episodes[episode_list][ep_no]})
        episode__ = Series_Episodes(episodes=s_season)
        episode__.episode_name = episodes_data['name']
        episode__.poster = episodes_data['no']
        episode__.movies = save_img(form.movie.data)
        episode__.movie_data = files.read()
        db.session.add(episode__)
        db.session.commit()

        return jsonify({

            'message': 'Added'
        })
    return render_template('episode.html', form=form)
@upload.route('/series')
def seri():
    series = Series.query.all()
    series_schema = SeriesSchema(many=True)
    result = series_schema.dump(series)
    series_ = Series_Season.query.all()
    series_season_schema = Series_SeasonSchema(many=True)
    res = series_season_schema.dump(series_)
    return jsonify({'data': result, 'season': res })
