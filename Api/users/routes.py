import datetime
import os
import jwt
from flask import *
from flask_login import login_user, logout_user, login_required
from Api.models import Users, UsersSchema, Data, DataSchema, Friend, FriendSchema, Activities, ActivitiesSchema, \
    Exciting, ExcitingSchema
from Api import db, bcrypt
from flask_cors import cross_origin
import cloudinary as Cloud
import cloudinary.uploader
from Api.utils import save_img
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Api.config import Config
from Api.ext import token_required

users = Blueprint('users', __name__)


# registering a user
@users.route('/api/sign_up', methods=['POST'])
@cross_origin()
def sign_up():
    data = request.get_json()
    name = data['name']
    dob = data['dob']
    phone_no = data['phone_no']
    country= data['country']
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
        users.phone_no = phone_no
        users.country= country
        users.password = hashed_password
        try:
            db.session.add(users)
            db.session.commit()
        except:
            return jsonify({
                "status": "error",
                "message": "Could not add user"
            }), 401

        return jsonify({
            "status": "success",
            "message": "User added successfully"
        }), 201



# logging in
@users.route('/api/login', methods=['GET', 'POST'])
@cross_origin()
def login(expires_sec=1800000000000):
    try:
        
        data = request.get_json()
        email = data['email']
        user = Users.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            login_user(user,  remember=True)
            session.permanent = True
            user.logged_in = True
            db.session.commit()
            #s = Serializer(Config.SECRET_KEY , expires_sec)
            payload= {
                    "id": user.id,  
                    "name": user.name,
                    'exp' : datetime.datetime.now() + datetime.timedelta(minutes = 300000),
                    "email": user.email
                }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
            data = jwt.decode(token, Config.SECRET_KEY, algorithms="HS256")

            return jsonify({'token' : token,
            "name":data['name'], "email": data['email']}), 201
        return jsonify({
            "message":
                'Could not verify user'}, 401)
                
    except:
        return jsonify({
            "message":
                'Sorry there is error on our end'},
                500
            
        )

                

@users.route('/api/select/genre', methods=['POST'])
@cross_origin()
@token_required
def select_genre(current_user):
    try:
        data = request.get_json()
        user = Data(love=current_user)
        for genre, value in data.items():
            setattr(user, genre, value)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "User's preferred genres have been saved."
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "An error occurred while processing your request.",
            "error": str(e)
        })
    

@users.route('/logout')
@cross_origin()
def logout_users():
    user = Users.query.filter_by(email=current_user.email).first()
    user.logged_in = False
    db.session.commit()
    logout_user()

    return redirect(url_for('api.home'))


# logging out
@users.route('/api/logout', methods=['POST'])
@cross_origin()
@token_required
def logout(current_user):
    user = Users.query.filter_by(email=current_user.email).first()
    user.logged_in = False
    db.session.commit()
    logout_user()
    # return redirect(url_for('api.home'))
    return jsonify({
        'message': 'logged out successfully'
    })


@users.route('/api/user/profile', methods=['POST'])
@cross_origin()
@token_required
def profile(current_user):
    try:
        # changing profile name
        data = request.get_json()
        if data:
            name = Users.query.filter_by(name=data['name']).first()
            if name and name != current_user:
                return jsonify({
                    "message": "This name is already used by another user",
                })
            elif current_user.name == data['name']:
                return jsonify({
                    "message": "You are currently using this name",
                })
            else:
                current_user.name = data['name']

        # uploading photo
        if 'picture' in request.files:
            try:
                profile_pics = save_img(request.files['picture'])
                current_user.profile = profile_pics
                user_photo = str(profile_pics).partition('.')
                if user_photo[-1] == 'jpg' or user_photo[-1] == 'png':
                    Cloud.uploader.upload(
                        f"{os.path.join(os.path.abspath('Api/static/movies/'), profile_pics)}",
                        chunk_size=6000000,
                        public_id=current_user.name,
                        overwrite=True,
                        eager=[
                            {"width": 300, "height": 300, "crop": "pad", "audio_codec": "none"},
                            {"width": 160, "height": 100, "crop": "crop", "gravity": "south",
                             "audio_codec": "none"}],
                        eager_async=True,
                        notification_url="https://mysite.example.com/notify_endpoint",
                        resource_type="image"
                    )
                else:
                    return jsonify({
                        "message": "Only image extensions allowed"
                    })
            except:
                return jsonify({
                    "message": "Error occurred while uploading image"
                })
        
        db.session.commit()
    except:
        return jsonify({
            "message": "Error occurred while updating profile"
        })

    name = current_user.name
    email = current_user.email
    dob = current_user.dob
    friends = Friend.query.filter_by(get=current_user).filter(Friend.u_friend != 'null').all()
    total = len(friends)

    return jsonify({
        "name": name,
        "email": email,
        "dob": dob,
        "friends": total
    })



# uploading a story
@users.route('/api/upload/story', methods=['POST'])
@cross_origin()
@token_required
def upload_story(current_user):
    data = request.get_json()
    file = request.files['story']
    socials = Activities(social=current_user)
    try:
        # add text as a table to the database
        socials.text = data['text']
    except:
        pass
    socials.story = data['name']
    socials.story_data = file.read()
    socials.time_uploaded = datetime.datetime.now()
    db.session.add(socials)
    db.session.commit()
    return jsonify({
        'message': 'uploaded'
    })


# list of current user's story
@users.route('/api/user/story', methods=['GET'])
@cross_origin()
@token_required
def my_story(current_user):
    socials = Activities.query.filter_by(social=current_user).all()
    activities_schema = ActivitiesSchema(many=True)
    result = activities_schema.dump(socials)

    return jsonify({
        "data": result
    })


# list of current user's friend's story
@users.route('/api/friend/story', methods=['GET'])
@cross_origin()
@login_required
def friend_story(current_user):
    friends = Friend.query.filter_by(get=current_user).all()
    for friend in friends:
        socials = Activities.query.filter_by(social=friend).all()
        activities_schema = ActivitiesSchema(many=True)
        result = activities_schema.dump(socials)

        return jsonify({
            "data": result
        })


# all users
@users.route('/api/users')
def user():
    pair = Users.query.all()
    users_schema = UsersSchema(many=True)
    result = users_schema.dump(pair)
    return jsonify(result)


# all users choice
@users.route('/api/data')
def datas():
    pair = Data.query.all()
    datas_schema = DataSchema(many=True)
    result = datas_schema.dump(pair)
    return jsonify(result)


@users.route('/api/_')
def s():
    pair = Exciting.query.all()
    datas_schema = ExcitingSchema(many=True)
    result = datas_schema.dump(pair)
    return jsonify(result)


# deleting all users
@users.route('/users', methods=['DELETE'])
def delete_users():
    pair = Users.query.all()
    for i in pair:
        db.session.delete(i)
        db.session.commit()
    return jsonify({
        'msg': 'deleted'
    })
