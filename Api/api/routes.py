import random
from flask import *
from flask_login import current_user, login_required
from Api import *
from Api.models import Movie, MovieSchema, Data, DataSchema, Friend, Users
from flask_cors import cross_origin

api = Blueprint('api', __name__)


# home
@api.route('/api/', methods=['GET'])
@cross_origin()
def home():
    movies = Movie.query.all()
    movie_schema = MovieSchema(many=True)
    result = movie_schema.dump(movies)
    if current_user.is_authenticated:
        id = current_user.id
        name = current_user.name
        return jsonify({
            "data": result,
            "user_id": id,
            "user_name": name
        }), 200
    return jsonify({
        "data": result,
        "message": "user not logged in"
    })


# searching for movie
@api.route('/api/search/movie', methods=['GET'])
@cross_origin()
def search():
    data = request.get_json()
    movie_name = Movie.query.filter_by(name=data['name']).first()
    if not movie_name:
        movie_name = Movie.query.filter_by(genre=data['genre']).first()
    if not movie_name:
        return jsonify({
            "message": " Could not find Name"
        }), 404
    else:
        movie_schema = MovieSchema()
        result = movie_schema.dump(movie_name)
        return jsonify({
            'data': result
        }), 200


# link to redirect to selected movie
# watching alone
@api.route('/api/get/movie/<string:u_id>/', methods=['GET'])
@cross_origin()
@login_required
def get_movie(u_id):
    movie_name = Movie.query.filter_by(public_id=u_id).first()
    movie_schema = MovieSchema()
    result = movie_schema.dump(movie_name)
    id = current_user.id
    name = current_user.name
    try:
        return jsonify({
            'data': result,
            "user_id": id,
            "user_name": name
        }), 200
    except:
        return jsonify({
            'message': "could not load data"
        })


# thumbs up a movie
@api.route('/api/like/movie/<string:u_id>', methods=['POST'])
@cross_origin()
@login_required
def like(u_id):
    movie = Movie.query.filter_by(public_id=u_id).first()
    movie.thumbs_up = movie.thumbs_up + 1
    loved_movie = Data(love=current_user, loved=movie.name)
    db.session.add(loved_movie)
    db.session.commit()
    return jsonify({
        'data': movie.thumbs_up
    })


# thumbs down movie
@api.route('/api/dislike/movie/<string:u_id>', methods=['POST'])
@cross_origin()
@login_required
def dislike(u_id):
    movie = Movie.query.filter_by(public_id=u_id).first()
    movie.thumbs_down = movie.thumbs_down + 1
    db.session.commit()
    return jsonify({
        'data': movie.thumbs_down
    })


# getting user's registered genre's choice for data processing
@api.route('/api/choice')
@login_required
def choice():
    d = []
    s = []
    datas = Data.query.filter_by(love=current_user).first()
    datas_schema = DataSchema()
    result = datas_schema.dump(datas)
    for key, value in result.items():
        if value == True:
            d.append(key)
            ''' for i in d:
        movie = Movie.query.filter_by(genre=i).all()[15]
        x = random.shuffle(movie)
        s.append(movie.name)

        return jsonify({
            "movies": s
        })'''
    try:
        d.remove('id')
    except:
        pass
    return jsonify({
        "preference": d
    })


# using user's interested movies for data processing
@api.route('/api/loved/movies')
def loved_movies():
    _love = []
    data = Data.query.filter_by(love=current_user).first()
    datas_schema = DataSchema()
    result = datas_schema.dump(data)
    for key, value in result.items():
        if key == 'loved':
            _love.append(value)
            random.shuffle(_love)
    return jsonify({
        'loved': _love
    })


# processing movies a user and his friend likes
@api.route('/api/my/friend/<string:name>/genres')
def i_and_my_friend(name):
    conjoin = []
    user = Users.query.filter_by(name=name).first()
    if user:
        friend = Friend.query.filter_by(get=current_user).filter_by(u_friend=name).first()
        if friend:
            _choice = Data.query.filter_by(love=current_user).first()
            friend_choice = Data.query.filter_by(love=user).first()
            datas_schema = DataSchema()
            result = datas_schema.dump(_choice)
            friend_result = datas_schema.dump(friend_choice)
            _list = [i for i in result.items()]
            friend_list = [i for i in friend_result.items()]
            for mine, _friend in zip(_list, friend_list):
                if mine[1] == True and _friend[1] == True:
                    conjoin.append(mine[0])

            # set(conjoin)
            return jsonify({
                "we both like ": conjoin
            })
        return jsonify({
            "message": f"{user} is not your friend"
        })
    return jsonify({"message": f"{name} not registered"})
