import datetime
import uuid
from Api.models import Room, RoomSchema, Users, UsersSchema, Friend, FriendSchema
from flask import Blueprint, request, url_for, jsonify
from Api import *
from flask_cors import cross_origin
from flask_login import current_user, login_required
from flask_socketio import emit, close_room, leave_room, join_room
from werkzeug.utils import redirect

chat = Blueprint('chat', __name__)


@chat.route('/api/add/friend/<string:name>', methods=['POST'])
@cross_origin()
@login_required
def add(name):
    add_friend = Users.query.filter_by(name=name).first()
    add_req = Users.query.filter_by(name=current_user.name).first()
    if add_friend:
        friends = Friend.query.filter_by(get=current_user).\
            filter_by(u_friend=add_friend.name).first()
        if friends:
            return jsonify \
                ({"message": f" you are already friends with {add_friend.name}"
                  })
        else:
            c_user = Friend(get=current_user, u_friend=add_friend.name)
            added_user = Friend(get=add_friend, u_friend=current_user.name)
            db.session.add(c_user)
            db.session.add(added_user)
            db.session.commit()
        return jsonify({"message": f"{add_req.name} is now friends with {add_friend.name}"
                        })
    return jsonify({
        'message': f"{name} not found"
    })


@chat.route("/all/friends")
def all_frnds():
    f = Friend.query.all()
    friend_schema = FriendSchema(many=True)
    result = friend_schema.dump(f)
    return jsonify({
        "data": result
    })


# Create room
@chat.route('/api/create/room', methods=['POST'])
@cross_origin
@login_required
def create_room():
    created_room = str(uuid.uuid4())
    host = current_user.name
    room = Room()
    room.unique_id = created_room
    room.host = host
    room.admin = True
    db.session.add(room)
    db.session.commit()

    return jsonify({
        "message": f"{created_room} created by {host}"
    })


@chat.route('/my/friends', methods=['GET'])
@cross_origin()
@login_required
def my_friends():
    friends = Friend.query.filter_by(get=current_user).all()
    friend_schema = FriendSchema(many=True)
    result = friend_schema.dump(friends)
    return jsonify({
        "data": result
    })


@chat.route('/api/my/rooms', methods=['GET'])
@cross_origin()
@login_required
def my_rooms():
    room = Room.query.filter_by(host=current_user.name).all()
    room_schema = RoomSchema(many=True)
    result = room_schema.dump(room)
    return jsonify({
        "data": result
    })


##########################################

@chat.route("/invite/friend/<string:name>")
def invite(name):
    user = Users.query.filter_by(name=name).first()
    pass

@chat.route('/')
@login_required
def sx():
    return jsonify({
        "message": 'room'
    })


@io.on("join_user") #, namespace='/sx')
def on_new_user(data):
    active = Room.query.filter_by(host='').first()
    name = current_user.name
    join_room(active.unique_id)
    emit("new_user", {"name": name}, userId=current_user.name, roomId=active.unique_id)


@io.on("leave")# , namespace='/sx')
def on_leave_room(data):
    active = Room.query.filter_by(host='').first()
    name = current_user.name
    leave_room(active.unique_id)
    emit("new_user", {"name": name}, roomId=active.unique_id)
    redirect(url_for("api.home"))


@io.on("close_room")#, namespace='/sx')
def on_close_room(data):
    active = Room.query.filter_by(host='').first()
    close_room(active.unique_id)
    db.session.delete(active.unique_id)
    redirect(url_for("api.home"))


@io.on("post_message")#, namespace='/sx')
def on_new_message(message):
    data = request.get_json()
    active = Room.query.filter_by(host='').first()
    emit("new_message", {
        "sender": current_user.name,
        "time": datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
        "data": data['message'],
    }, room=active.unique_id, broadcast=True)
