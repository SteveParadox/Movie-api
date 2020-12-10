import shortuuid
import uuid
from flask import *
from flask_login import current_user, login_required, login_user, logout_user
from Api import *
from Api.models import Movie, MovieSchema, Users, UsersSchema, Friend, Room
from flask_cors import CORS, cross_origin
from .form import LoginForm, Sign_Up
raw = Blueprint('raw', __name__)

@raw.route('/users')
@login_required
def all():
    pair = Users.query.filter(Users.email != current_user.email).all()
    return render_template('users.html' , pair=pair)

@raw.route('/sign_up', methods=['GET', 'POST'])
def reg():
    form = Sign_Up()
    if form.validate_on_submit():
        users = Users()
        users.name = form.name.data
        users.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        users.dob = form.dob.data
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            return jsonify({
                "message": "User already registered"
            })
        users.email = form.email.data
        db.session.add(users)
        db.session.commit()
        return redirect(url_for('raw.login_users'))
    return render_template('sign_up.html', form=form)


@raw.route('/login', methods=['GET', 'POST'])
def login_users():
    if current_user.is_authenticated:
        return redirect(url_for('raw.home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('raw.home_page'))
        else:
            flash('Login failed. please check email and password', 'danger')
        if current_user.is_authenticated:
            return redirect(url_for('raw.home_page'))
    return render_template('login.html', form=form)


@raw.route('/home', methods=['GET'])
def home_page():
    try:
        movie = Movie.query.all()[1]
        movie1 = Movie.query.all()[2]
        movie2 = Movie.query.all()[3]
        movie4 = Movie.query.all()[4]
        movie5 = Movie.query.all()[5]
        movie6 = Movie.query.all()[6]
        movie7 = Movie.query.all()[0]
        movies = Movie.query.all()
        return render_template('index.html', movie1=movie1, movie2=movie2, movie4=movie4,
                               movies=movies,movie=movie, movie5=movie5, movie6=movie6, movie7=movie7
                               )
    except:
        return render_template('index.html')


@raw.route('/movie/<string:u_id>', methods=['GET', 'POST'])
@login_required
def movie_show(u_id):
    movie= Movie.query.filter_by(public_id=u_id).first()
    movies = Movie.query.filter(Movie.public_id is not u_id).all()
    return render_template('movie.html', movie=movie, movies=movies)

@raw.route('/')
@login_required
def chat():

    return render_template('rooms.html')



@raw.route('/my/friends', methods=['GET'])
@login_required
def my_frnds():
    friends = Friend.query.filter_by(get=current_user).all()
    return render_template('frnd.html', friends=friends)



@raw.route('/create/room/for/<string:movie>', methods=['GET', 'POST'])
@login_required
def crt_room(movie):
    created_room = str(uuid.uuid4())
    movie = Movie.query.filter_by(public_id=movie).first()
    host = current_user.name
    room = Room()
    room.unique_id = created_room
    room.host = host
    room.admin = True
    db.session.add(room)
    db.session.commit()
    return redirect(url_for('raw.watching', movie_id=movie.public_id, room=created_room))


@raw.route('/watch/<string:movie_id>/in/room/<string:room>', methods=['GET'])
@login_required
def watching(movie_id, room):
    movie = Movie.query.filter_by(public_id=movie_id).first()
    room = Room.query.filter_by(unique_id=room).first()
    return render_template('rooms.html', movie=movie, room=room)


@raw.route('/xc')
def fpd():
    db.drop_all(app=create_app())
    db.create_all(app=create_app())
    return 'done'
