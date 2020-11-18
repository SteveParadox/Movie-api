import datetime

from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from Api.models import Users, UsersSchema, Data, DataSchema, Friend, FriendSchema
from Api import db, bcrypt
from flask_cors import cross_origin

from Api.utils import save_img

users = Blueprint('users', __name__)


# registering a user
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
@users.route('/api/login')
@cross_origin()
def login():
    data = request.get_json()
    email = data['email']
    user = Users.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        user.logged_in = True
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "login successful",
            "data": {
                "id": user.id,
                "name": user.name
            }
        }), 200
    return jsonify({
        "status": "failed",
        "message": "Failed getting user"
    }), 401


# registering user's preferred genre for data processing
@users.route('/api/select/genre', methods=['POST'])
@cross_origin()
@login_required
def genre():
    data = request.get_json()
    action = data['action']
    comedy = data['comedy']
    horror = data['horror']
    documentary = data['documentary']
    mystery = data['mystery']
    animation = data['animation']
    sci_fi = data['sci-fi']
    romance = data['romance']
    erotic = data['erotic']
    fantasy = data['fantasy']
    drama = data['drama']
    thriller = data['thriller']
    para_normal = data['para-normal']
    family = data['family']
    try:
        user = Data(love=current_user)
        user.action = action
        user.comedy = comedy
        user.horror = horror
        user.documentary = documentary
        user.mystery = mystery
        user.animation = animation
        user.sci_fi = sci_fi
        user.romance = romance
        user.erotic = erotic
        user.fantasy = fantasy
        user.drama = drama
        user.thriller = thriller
        user.para_normal = para_normal
        user.family = family
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "committed"
        })
    except:
        return jsonify({

            "message": 'error'
        })


@users.route('/logout')
@cross_origin()
@login_required
def logout_users():
    user = Users.query.filter_by(email=current_user.email).first()
    user.logged_in = False
    db.session.commit()
    logout_user()

    return redirect(url_for('api.home'))


# logging out
@users.route('/api/logout', methods=['POST'])
@cross_origin()
@login_required
def logout():
    user = Users.query.filter_by(email=current_user.email).first()
    user.logged_in = False
    db.session.commit()
    logout_user()
    # return redirect(url_for('api.home'))
    return jsonify({
        'message': 'logged out successfully'
    })


# getting profile of a user
@users.route('/api/user/profile', methods=['GET'])
@cross_origin()
@login_required
def profile():
    profile_pics = save_img(request.files['picture'])
    current_user.profile = profile_pics
    db.session.commit()
    name = current_user.name
    email = current_user.email
    image_file = url_for('static', filename='movies/' + current_user.profile)
    friends = Friend.query.filter_by(get=current_user).filter(Friend.u_friend != 'null').all()
    total = len(friends)

    return jsonify({
        "name": name,
        'email': email,
        'image': image_file,
        'frends': total
    })


# uploading a story
@users.route('/api/upload/story', methods=['POST'])
@cross_origin()
@login_required
def upload_story():
    data = request.get_json()
    file = request.files['movie']
    friend = Friend(get=current_user)
    friend.story = data['name']
    user.story_data = file.read()
    friend.time_uploaded = datetime.datetime.now()
    db.session.add(friend)
    db.session.commit()
    return jsonify({
        'message': 'uploaded'
    })


# list of current user's story
@users.route('/api/user/story', methods=['GET'])
@cross_origin()
@login_required
def my_story():
    user = Friend.query.filter_by(get=current_user).filter(Friend.u_friend == 'null').all()
    friend_schema = FriendSchema(many=True)
    result = friend_schema.dump(user)


# list of current user's friend's story
@users.route('/api/friend/story', methods=['GET'])
@cross_origin()
@login_required
def friend_story():
    pass


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
