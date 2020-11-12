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
    my_movies = Movie.query.filter().all()
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


@api.route('/api/rate/movie', methods=['POST'])
@cross_origin()
def rate():

    pass