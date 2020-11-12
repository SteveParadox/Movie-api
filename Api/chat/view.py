import datetime
import uuid

from Api import io, db
from Api.models import Room, RoomSchema, Users, UsersSchema, Friend, FriendSchema, Movie
from flask import Blueprint, request, url_for, jsonify, render_template
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
        friends = Friend.query.filter_by(get=current_user). \
            filter_by(u_friend=add_friend.name).first()
        if friends:
            return jsonify(
                {
                    "message": f" you are already friends with {add_friend.name}"
                }
            )
        else:
            if add_req.name == current_user.name:
                return jsonify(
                    {
                        "message": "You cannot add your self"
                    }
                )

            c_user = Friend(get=current_user, u_friend=add_friend.name)
            added_user = Friend(get=add_friend, u_friend=current_user.name)
            db.session.add(c_user)
            db.session.add(added_user)
            db.session.commit()
        return jsonify(
            {"message": f"{add_req.name} is now friends with {add_friend.name}"
             })
    return jsonify(
        {
            'message': f"{name} not found"
        }
    )


@chat.route('/add/friend/<string:name>', methods=["GET", 'POST'])
@login_required
def add_(name):
    add_friend = Users.query.filter_by(name=name).first()
    add_req = Users.query.filter_by(name=current_user.name).first()
    if add_friend:
        friends = Friend.query.filter_by(get=current_user). \
            filter_by(u_friend=add_friend.name).first()
        if friends:
            return jsonify(
                {
                    "message": f" you are already friends with {add_friend.name}"
                }
            )
        else:
            if add_req.name == current_user.name:
                return jsonify(
                    {
                        "message": "You cannot add your self"
                    }
                )
            c_user = Friend(get=current_user, u_friend=add_friend.name)
            added_user = Friend(get=add_friend, u_friend=current_user.name)
            db.session.add(c_user)
            db.session.add(added_user)
            db.session.commit()
        return jsonify(
            {"message": f"{add_req.name} is now friends with {add_friend.name}"
             })
    return jsonify(
        {
            'message': f"{name} not found"
        }
    )


@chat.route('/api/my/friends', methods=['GET'])
@cross_origin()
@login_required
def my_friends():
    friends = Friend.query.filter_by(get=current_user).all()
    friend_schema = FriendSchema(many=True)
    result = friend_schema.dump(friends)
    return jsonify(
        {
            "data": result
        }
    )


@chat.route("/all/friends")
def all_frnds():
    f = Friend.query.all()
    friend_schema = FriendSchema(many=True)
    result = friend_schema.dump(f)
    return jsonify(
        {
            "data": result
        }
    )


# Create room
@chat.route('/api/create/room/for/<string:movie>', methods=['POST'])
@cross_origin()
@login_required
def create_room(movie):
    created_room = str(uuid.uuid4())
    movie = Movie.query.filter_by(public_id=movie).first()
    host = current_user.name
    room = Room()
    room.unique_id = created_room
    room.host = host
    room.admin = True
    db.session.add(room)
    db.session.commit()

    '''return jsonify(
        {
            "message": f"Room {created_room} created by {host} ",
            "movie": movie.movies,
            "movie name": movie.name
        }
    )'''
    return redirect(url_for('chat.watch', movie=movie.public_id, room=created_room))


# redirecting to the room id
@chat.route('/api/watch/<string:movie>/in/room/<string:room>', methods=['GET'])
@login_required
def watch(movie, room):
    print(movie)
    movie = Movie.query.filter_by(public_id=movie).first()
    room = Room.query.filter_by(unique_id=room).first()
    return jsonify(
        {

            "movie": movie.movies,
            "movie name": movie.name,
            'room': room.unique_id
        }
    )


@chat.route('/api/my/rooms', methods=['GET'])
@cross_origin()
@login_required
def my_rooms():
    room = Room.query.filter_by(host=current_user.name).all()
    room_schema = RoomSchema(many=True)
    result = room_schema.dump(room)
    return jsonify(
        {
            "data": result
        }
    )


@chat.route('/api/my/rooms/delete/<string:room_id>', methods=['POST'])
@cross_origin()
@login_required
def delete_room(room_id):
    room = Room.query.filter_by(host=current_user.name).filter_by(unique_id=room_id).first()
    if room:
        db.session.delete(room)
        db.session.commit()
        return jsonify(
            {
                "data": f"{room.unique_id} deleted"
            }
        )
    return jsonify(
        {
            "message": "error"
        }
    )


## socket server
##########################################

@chat.route("/invite")
def invite(name):
    user = Users.query.filter_by(name=name).first()
    pass


@io.on("connect", namespace='/chat')
def on_connect(data):
    return jsonify({'message': 'connected'})


@io.on('disconnect', namespace='/chat')
def disconnect():
    return jsonify({'message': 'disconnected'})


@io.on_error(namespace='/room')
def chat_error_handler(e):
    print('An error has occurred: ' + str(e))


@io.on('online')
def online(data):
    emit('status_change', {'username': data['username'], 'status': 'online'}, broadcast=True)


@io.on('offline')
def offline(data):
    emit('status_change', {'username': data['username'], 'status': 'offline'}, broadcast=True)


@io.on('Offer')
def SendOffer(offer):
    emit('BackOffer', offer)


@io.on('Answer')
def SendAnswer(data):
    emit('BackAnswer', data)


# join room
@io.on("join_user", namespace='/chat')
def on_new_user(data):
    room = request.get_json()
    active = Room.query.filter_by(unique_id=room['room']).first()
    name = current_user.name
    join_room(active.unique_id)
    emit("New user", {"name": name}, room=active.unique_id, broadcast=True)


'''@io.on('my event')
def handle_event(json):
    print('recieved' + str(json))
    io.emit('response', json)'''


@io.on('movie')
def handle_movie(json):
    print('recieved' + str(json))
    io.emit('watch', json)


# leave room
@io.on("leave_user", namespace='/chat')
def on_leave_room(data):
    room = request.get_json()
    active = Room.query.filter_by(unique_id=room['room']).first()
    name = current_user.name
    leave_room(active.unique_id)
    emit("New user", {"name": name}, room=active.unique_id, broadcast=True)
    redirect(url_for("api.home"))


# close room
@io.on("close_room", namespace='/chat')
def on_close_room(data):
    room = request.get_json()
    active = Room.query.filter_by(host=current_user.name) \
        .filter_by(admin=True) \
        .filter_by(unique_id=room['room']).first()
    close_room(active.unique_id)
    db.session.delete(active.unique_id)
    redirect(url_for("api.home"))


@io.on("video_chat", namespace='/chat')
def on_video_chat(data):
    room = request.get_json()
    active = Room.query.filter_by(unique_id=room['room']).first()
    pass


# watch movie
@io.on("watch_movie", namespace='/chat')
def on_video_stream(data):
    room = request.get_json()
    active = Room.query.filter_by(unique_id=room['room']).first()
    host = active.host
    movie_ = Movie.query.filter_by(public_id=room['u_id']).first()
    emit("Watch", {
        "host": host,
        "movie": movie_.movies,
    }, room=active.unique_id, broadcast=True)


# send message
@io.on("post_message", namespace='/chat')
def on_new_message(message):
    data = request.get_json()
    active = Room.query.filter_by(unique_id=data['room']).first()
    emit("New message", {
        "sender": current_user.name,
        "time": datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
        "data": data['message'],
    }, room=active.unique_id, broadcast=True)

    ##########################################################
    '''def send_data(self, frame, text):
        cur_t = time.time()
        if cur_t - self._last_update_t > self._wait_t:
            self._last_update_t = cur_t
            frame = edgeiq.resize(
                    frame, width=640, height=480, keep_scale=True)
            sio.emit(
                    'cv2server',
                    {
                        'image': self._convert_image_to_jpeg(frame),
                        'text': '<br />'.join(text)
                    })'''
