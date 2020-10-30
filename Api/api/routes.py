import uuid
import os
import shortuuid
from flask import Blueprint, jsonify, render_template
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, StringField, SubmitField
from wtforms.validators import DataRequired
from Api import *
from Api.models import Movie, MovieSchema, Users, UsersSchema
from Api.utils import save_img
import requests
import json
from flask_cors import CORS, cross_origin

api = Blueprint('api', __name__)


@api.route('/api/', methods=['GET'])
@cross_origin()
def home():
    id= ''
    name = ''
    movies = Movie.query.all()
    movie_schema = MovieSchema(many=True)
    result = movie_schema.dump(movies)
    if current_user.is_authenticated:
        id= current_user.id
        name= current_user.name
        return jsonify({
        "data" : result,
      
            "user_id" : id,
            "user_name" : name
        }), 200
    return jsonify({
          "data" : result,
    "message" : "user not found"
    })


@api.route('/', methods=['GET'])
def home_page():
    movie= Movie.query.all()
    return render_template('home.html', movie=movie)


#searching for movie
@api.route('/api/search/movie', methods=['POST'])
@cross_origin()
def search():
    from urllib import request
    data = request.get_json()
   # print(data["name"])
    movie_name = Movie.query.filter_by(name=data['name']).first()
    if not movie_name:
        return jsonify({
            "message": " Could not find Name"
        }), 404
    else:
        movie_schema = MovieSchema()
        result = movie_schema.dump(movie_name)
        return jsonify({
            'name': result['name'],
            'description': result['description'],
            'review': result['review'],
            'poster': result['poster'],
            #'movies': result['movies']
        }), 200
      
#link to redirect to selected movie
#watching alone
@api.route('/api/get/movie/<string:u_id>/', methods=['GET'])
@cross_origin()
def get_movie(u_id):
    movie_name = Movie.query.filter_by(public_id=u_id).first()
    movie_schema = MovieSchema()
    result = movie_schema.dump(movie_name)
    #user= Users.query.filter_by(name=current_user.name).first()  
    id = current_user.id
    name = current_user.name
    try:
      return jsonify({
          'data' : result,
          "user_id": id,
          "user_name": name
      }), 200
    except:
      return jsonify({
        'message' : "could not load data"
      })

@api.route('/api/user/connect/<string:friend>')
@cross_origin()
def connect(friend):
    pair= Users.query.filter_by(id=current_user.id).first()
    users_schema = UsersSchema()
    result = users_schema.dump(pair)
    d= {'data' : result}
    f=d['data']
    o=f['pair']
    return jsonify(o)
    '''d= []
    host= Users.query.filter_by(name=current_user.name).first()
    for others in sec_user:
        sec_user= Users.query.filter_by(name=others).first()
        user= Users()
        user.pair= str(shortuuid() + str(d.append(host, sec_user)) )
        db.session.commit()'''
                                   
@api.route('/api/watch/<string:u_id>')
@cross_origin()
def watch(u_id):        
    movie =  Movie.query.filter_by(unique_id=u_id).first()                                
    list = Users.query.filter(current_user in Users.pair).all()
    if list:
        return jsonify({
        'name':[i[1:] for i in list]
        })                               
