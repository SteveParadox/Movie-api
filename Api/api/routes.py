import datetime
import uuid
import os
import shortuuid

from flask import Blueprint, jsonify, render_template, url_for, request
from flask_login import current_user, login_required
from Api import *
from Api.models import Movie, MovieSchema, Users, UsersSchema, Friend, Room
from flask_cors import CORS, cross_origin

api = Blueprint('api', __name__)


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
        "message": "user not found"
    })


@api.route('/home', methods=['GET'])
def home_page():
    try:
        movie = Movie.query.all()[0]
        movie1 = Movie.query.all()[1]
        movie2 = Movie.query.all()[2]
        movie4 = Movie.query.all()[4]
        movie5 = Movie.query.all()[5]
        movie6 = Movie.query.all()[6]
        movie7 = Movie.query.all()[7]
        movies = Movie.query.all()
        return render_template('index.html', movie=movie, movie1=movie1, movie2=movie2, movie4=movie4,
                               movies=movies, movie5=movie5, movie6=movie6, movie7=movie7
                               )
    except:
        return render_template('index.html')



# searching for movie
@api.route('/api/search/movie', methods=['POST'])
@cross_origin()
def search():
    data = request.get_json()
    movie_name = Movie.query.filter_by(name=data['name']).first()
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
