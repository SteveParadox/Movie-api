import random
from flask import *
from Api import *
from Api.models import Movie, MovieSchema, Data, DataSchema, Friend, Users, Exciting, Store, UserRating
from flask_cors import cross_origin
from functools import wraps
import jwt
from Api.ext import token_required

api = Blueprint('api', __name__)


@api.route('/api/home', methods=['GET'])
@cross_origin()
def home():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.paginate(page=page, per_page=10)
    movie_schema = MovieSchema(many=True)
    result = movie_schema.dump(movies.items)
    return jsonify({
        "data": result,
        "message": "user not logged in",
        'logged in': False
    }), 200

# home
@api.route('/api/', methods=['POST'])
@token_required
@cross_origin()
def loggedHome(current_user):
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.paginate(page=page, per_page=10)
    movie_schema = MovieSchema(many=True)
    result = movie_schema.dump(movies.items)
    if current_user:
        id = current_user.id
        name = current_user.name
        email = current_user.email
        friends = Friend.query.filter_by(get=current_user).filter(Friend.u_friend != 'null').all()
        friend = len(friends)
        return jsonify({
            "data": result,
            "user_id": id,
            "user_name": name,
            'user_image': name,
            "email": email,
            'friends': friend,
            'logged in': True
        }), 200
    return jsonify({
        "message": "user not logged in",
        'logged in': False
    })



@api.route('/api/genres', methods=['POST'])
@cross_origin()
def get_movies_by_genre():
    data = request.get_json()
    genre_list = data['genres']
    movies = Movie.query.filter(Movie.genre.in_(genre_list)).all()
    result_list = []
    for movie in movies:
        result_list.append(movie.name)
    return jsonify({
        "movies": result_list
    }), 200




@api.route('/api/search/movie', methods=['POST'])
@cross_origin()
def searchList():
    data = request.get_json()
    search_term = str(data['name'][0]).upper() + data['name'][1:]
    movies = Movie.query.filter(
        (Movie.name.ilike(f'%{search_term}%')) |
        (Movie.genre.ilike(f'%{search_term}%')) |
        (Movie.creator.ilike(f'%{search_term}%'))
    ).all()

    if not movies:
        return jsonify({
            "message": "Could not find Name"
        }), 404

    movie_schema = MovieSchema(many=True)
    result = movie_schema.dump(movies)
    return jsonify({
        'data': result
    }), 200



# link to redirect to selected movie
# watching alone
@api.route('/api/get/movie/<string:u_id>/', methods=['POST'])
@cross_origin()
@token_required
def get_movie(current_user, u_id):
    try:
        movie_name = Movie.query.filter_by(public_id=u_id).first()
        movie_name.popular += 1
        db.session.commit()
        movie_schema = MovieSchema()
        result = movie_schema.dump(movie_name)
        id = current_user.id
        name = current_user.name
        return jsonify({
            'data': result,
            "user_id": id,
            "user_name": name
        }), 200
    except AttributeError:
        return jsonify({
            'message': "Could not find the movie"
        }), 404
    except:
        return jsonify({
            'message': "Server error"
        }), 500


@api.route('/api/similar/movie/<string:u_id>', methods=['GET'])
@cross_origin()
def similar_movie(u_id):
    try:
        movie = Movie.query.filter_by(public_id=u_id).first()
        genres = movie.genre
        movies = [m for m in Movie.query.all() if any(g in genres for g in m.genre)]
        similarList = [{
            "name": m.name,
            "id": m.public_id,
            "genre": m.genre,
            "overview": m.description
        } for m in movies if m.public_id != u_id]
        return jsonify({
            "data": similarList
        }), 200
    except:
        return jsonify({
            "message": "Could not find movie with the given public ID."
        }), 404


# thumbs up a movie
@api.route('/api/like/movie/<string:u_id>', methods=['POST'])
@cross_origin()
@token_required
def likeMovie(current_user, u_id):
    movie = Movie.query.filter_by(public_id=u_id).first()
    movie.thumbs_up = movie.thumbs_up + 1
    loved_movie = Exciting(rate=current_user, loved=movie.name)
    db.session.add(loved_movie)
    db.session.commit()
    return jsonify({
        'data': movie.thumbs_up
    })



# getting user's registered genre's choice for data processing
@api.route('/api/choice', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
@token_required
def choicesUser(current_user):
    selected_genres = []
    suggested_result =[]
    try:
        datas = Data.query.filter_by(love=current_user).all()
        datas_schema = DataSchema(many=True)
        result = datas_schema.dump(datas)
        for i in result:
            for key, value in i.items():
                if value == True:
                    selected_genres.append(key)
        try:
            
            selected_genres.remove('id')
            selected_genres.remove('love')
        except:
            pass
        movies= Movie.query.all()
        for i,h in zip(selected_genres, movies):  
            if str(i[0].upper())+i[1:] in h.genre:
                suggested_result.append({
                    'name': h.name,
                    'id': h.public_id,
                    "genre": h.genre,
                    'overview': h.description,

                })

        return jsonify({
            "data": suggested_result
        })
    except:
        return jsonify({
            "message": "Not Logged In"
        })



@api.route('/api/loved/movies', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
@token_required
def loved_movies(current_user):
    result = []
    t = []
    
    # Get all movies that the user has liked
    liked_movies = Exciting.query.filter_by(rate=current_user).all()
    for liked in liked_movies:
        liked_movie = Movie.query.filter_by(name=liked.loved).first()
        if liked_movie:
            # Get all movies that have the same genre as the liked movie
            movies = Movie.query.filter_by(genre=liked_movie.genre).all()
            for movie in movies:
                t.append({
                    'name': movie.name,
                    'genre': movie.genre,
                    'id': movie.public_id,
                    'overview': movie.description,
                })
        
    return jsonify({
        'data': t
    })




# suggesting movies a user and his friend likes
@api.route('/api/my/friend/<string:name>/suggest', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
@token_required
def i_and_my_friend(name):
    conjoin = []
    suggested_movies = []
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
                if mine[1] and _friend[1]:
                    conjoin.append(mine[0])
            for genres in conjoin:
                movies = Movie.query.filter_by(genre=f'{genres[0].upper() + genres[1:]}').all()
                for index, movie in enumerate(movies):
                    suggested_movies.append({
                        'name': movie.name,
                        'id': movie.public_id,
                        'genre': movie.genre,
                        'runtime ': movie.runtime,
                        'overview': movie.description
                    })
            random.shuffle(suggested_movies)
            return jsonify({
                'we both like': suggested_movies
            })
        else:
            return jsonify({
                'message': f'{name} is not your friend'
            })
    else:
        return jsonify({
            'message': f'{name} is not registered'
        })


@api.route('/api/add/review/<string:movie_id>', methods=['POST'])
@cross_origin()
@token_required
def addRating(current_user, movie_id):
    try:
        data=request.get_json()
        movies = Movie.query.filter_by(public_id=movie_id).first()
        ratings = UserRating(reviews=current_user, reviewing=movies)
        ratings.rating = int(data["rating"])
        db.session.add(ratings)
        db.session.commit()

        return jsonify({
            "message": "rated"
        })
    except:
        return jsonify({
            "message":"Error adding to database"
        })



@api.route('/api/post/review/<string:movie_id>', methods=['POST'])
@cross_origin()
@token_required
def addReviews(current_user, movie_id):
    try:
        data=request.get_json()
        movies = Movie.query.filter_by(public_id=movie_id).first()
        ratings = UserReview(reviews=current_user, reviewing=movies)
        ratings.rating = int(data["rating"])
        db.session.add(ratings)
        db.session.commit()

        return jsonify({
            "message": "rated"
        })
    except:
        return jsonify({
            "message":"Error adding to database"
        })

@api.route('/api/reviews/<string:movie_id>', methods=['GET'])

def movieRating(movie_id):
    try:
        movies = Movie.query.filter_by(public_id=movie_id).first()
        ratings = UserRating.query.filter_by(reviewing=movies).first()
        return jsonify({
            "movie": movies.name,
            "rating": ratings.rating,
            "public_id": movies.public_id,
            "overview": movies.description,
            "genre": movies.genres
        })
    except:
        return jsonify({
            "message": "Movie has no rating"
        })


@api.route('/api/popular')
@cross_origin()
def popularMovies():
    movies = Movie.query.order_by(Movie.review.desc()).all()
    movie_schema = MovieSchema(many=True)
    result = movie_schema.dump(movies)
    return jsonify({
        "data": result,
    }), 200


@api.route('/api/trending')
@cross_origin()
def trending():
    movies = Movie.query.order_by(Movie.popular.desc()).all()
    movie_schema = MovieSchema(many=True)
    result = movie_schema.dump(movies)
    return jsonify({
        "data": result,
    }), 200


@api.route('/api/add/list/<string:movie_id>', methods=['POST'])
@cross_origin()
@token_required
def add_to_list(current_user, movie_id):
    movie = Movie.query.filter_by(public_id=movie_id).first()
    store = Store(saved=current_user)
    store.stored_data = movie.public_id
    db.session.add(store)
    db.session.commit()
    return jsonify({
        "data": 'committed',
    }), 200


@api.route('/api/my/list')
@cross_origin()
@token_required
def my_list(current_user):
    store = Store.query.filter_by(saved=current_user).all()
    data = []
    for movie_id in store:
        movies = Movie.query.filter_by(public_id=movie_id.stored_data).all()
        for movie in movies:
            data.append({'name': movie.name,
                         'genre': movie.genre,
                         'id': movie.public_id,
                         'overview': movie.description,
                         })
    return jsonify({
        "data": data,
    }), 200
