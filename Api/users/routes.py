import uuid
import os
import shortuuid
from Api import *


from flask import *
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, DateField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from Api import *
from Api.models import Movie, MovieSchema, Users, UsersSchema
from Api.utils import save_img
import requests
import json
from flask_cors import CORS, cross_origin

users = Blueprint('users', __name__)


# registering
@users.route('/api/sign_up', methods=['POST'])
@cross_origin()
def sign_up():
    data = request.get_json()
    name = data['name']
    dob = data['dob']
    email = data['email']
    password = data['password']
    user = Users.query.filter_by(email=email).first()
    if user:
        return jsonify({
            "message": "User already registered"
        })
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users = Users()
        users.name = name
        users.dob = dob
        users.email = email
        users.password = hashed_password
        users.pair=[]

        try:
            db.session.add(users)
            db.session.commit()

        except:
            return jsonify({
                "status": "error",
                "message": "Could not add user"
            })

        return jsonify({
            "status": "success",
            "message": "User added successfully"
        }), 201

    # registering user's preferred genre


class Sign_Up(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    dob = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit ')

class LoginForm(FlaskForm):
    email= StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit ')

@users.route('/sign_up', methods=['GET', 'POST'])
def reg():
    form = Sign_Up()
    if  form.validate_on_submit():
        users= Users()
        users.name=form.name.data
        users.email= form.email.data
        users.password=  bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        users.dob= form.dob.data
        db.session.add(users)
        db.session.commit()
        return redirect(url_for('users.login_users'))
    return render_template('sign_up.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login_users():
    if current_user.is_authenticated:
        return redirect(url_for('api.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('api.home'))
        else:
            flash('Login failed. please check email and password', 'danger')
        if current_user.is_authenticated:
            return redirect(url_for('api.home'))
    return render_template('login.html', form=form)



@users.route('/api/sign_up/genre', methods=['POST'])
def genre():
    pass


# logging in
@users.route('/api/login')
@cross_origin()
def login():
    data = request.get_json()
    name = data['name']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = Users.query.filter_by(name=name).first()
    if not user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({
            "status": "failed",
            "message": "Failed getting user"
        }), 401
    login_user(user)
    return jsonify({
        "status": "success",
        "message": "login successful",
        "data": {
            "id": user.id,
            "name": user.name
        }
    }), 200
@users.route('/logout', methods=['POST'])
def logout_users():
    logout_user()
    return redirect(url_for('api.home_page'))

# logging out
@users.route('/api/logout', methods=['POST'])
@cross_origin()
def logout():
    logout_user()
    return jsonify({
        'message': 'logged out successfully'
    })

@users.route('/users')
@cross_origin()
def user():
    pair= Users.query.all()
    users_schema = UsersSchema(many=True)
    result = users_schema.dump(pair)
    return jsonify(result)


@users.route('/users', methods=['DELETE'])
def delete_users():
    pair= Users.query.all()
    for i in pair:
        db.session.delete(i)
        db.session.commit()
    return jsonify({
        'msg' : 'deleted'
    })

@users.route('/api/add/friend/<string:name>', methods=['POST'])
@cross_origin()
def add(name):
    d=[]
    x=[]
    friend = Users.query.filter_by(name=name).first()
    if friend:
        add= Users.query.filter_by(id=current_user.id).first()
        x.append(name)
        d.append(current_user.name)
        add.pair=x
        friend.pair=d
        db.session.commit()
        return jsonify({
            'message' : 'Friend added successfully'
        })
    return jsonify({
        'message' : f"{name} not found"
    })