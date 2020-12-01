import uuid
from flask import *
from flask_cors import cross_origin
from flask_login import current_user, login_required
from flask_socketio import emit, close_room, leave_room, join_room

from Api import *
from Api.models import Room, RoomSchema, Users, Friend, FriendSchema, Movie, Vote, Room_Activities

chat = Blueprint('chat', __name__)

store = []
online_friend = []


# adding a friend to watch with
@chat.route('/api/add/friend/<string:name>', methods=["GET", 'POST'])
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
            if add_friend.name == current_user.name:
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
    ), 404


@chat.route('/api/remove/friend/<string:name>', methods=["GET", 'POST'])
@cross_origin()
@login_required
def remove_(name):
    remove_friend = Users.query.filter_by(name=name).first()
    add_req = Users.query.filter_by(name=current_user.name).first()
    if remove_friend:
        friends = Friend.query.filter_by(get=current_user). \
            filter_by(u_friend=remove_friend.name).first()
        if not friends:
            return jsonify(
                {
                    "message": f" you are not friends with {remove_friend.name}"
                }
            )
        else:
            if remove_friend.name == current_user.name:
                return jsonify(
                    {
                        "message": "You cannot unfriend your self"
                    }
                )
            c_user = Friend.query.filter_by(get=current_user, u_friend=remove_friend.name).first()
            added_user = Friend.query.filter_by(get=remove_friend, u_friend=current_user.name).first()
            db.session.delete(c_user)
            db.session.delete(added_user)
            db.session.commit()
        return jsonify(
            {"message": f"{add_req.name} is no more friends with {remove_friend.name}"
             })
    return jsonify(
        {
            'message': f"{name} not found"
        }, 404
    )


# all friends of a particular user
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


# all friends of all users
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
@chat.route('/api/watch/<string:movie_id>/in/room/<string:room>', methods=['GET'])
@login_required
def watch(movie_id, room):
    movie = Movie.query.filter_by(public_id=movie_id).first()
    room = Room.query.filter_by(unique_id=room).first()
    if room:

        store.append(room.unique_id)
        return jsonify(
            {

                "movie": movie.movies,
                "movie name": movie.name,
                'room': room.unique_id,
                'image': movie.poster
            }
        )
    else:
        return jsonify({
            'message': 'Error... not found'
        }), 404

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


@io.on("connect")
def on_connect():
    io.emit('resp', {'message': 'connected'})


# join room
@io.on("join_user")
def on_new_user(data):
    room = data['room']
    print(data)
    active_ = Room.query.filter_by(unique_id=room).first()
    print(active_.unique_id)
    name = current_user.name
    join_room(active_.unique_id)
    io.emit("new_user",
         {"name": name, 'room': active_.unique_id},
         room=active_.unique_id, broadcast=True)


# leave room
@io.on("leave_room")
def on_leave_room(data):
    room = data['room']
    active = Room.query.filter_by(unique_id=room).first()
    name = current_user.name
    if name == active.host:
        close_room(active.unique_id)
        db.session.delete(active.unique_id)
        return redirect(url_for("api.home"))
    leave_room(active.unique_id)
    io.emit("Left_user", {"message": f"{name} has left the room"}, room=active.unique_id, broadcast=True)
    return redirect(url_for("api.home"))


# close room
@io.on("close_room")
def on_close_room(data):
    room = data['data']
    active = Room.query.filter_by(host=current_user.name) \
        .filter_by(admin=True) \
        .filter_by(unique_id=room).first()
    close_room(active.unique_id)
    db.session.delete(active.unique_id)
    return redirect(url_for("api.home"))


# watch movie
@io.on('watch_movie')
def on_video_stream(data):
    room = data['room_id']
    movie = data['movie_id']
    active = Room.query.filter_by(unique_id=room).first()
    r_activities = Room_Activities(activity=active)
    r_activities.movie = movie
    db.session.add(r_activities)
    db.session.commit()
    host = active.host
    movie_ = Movie.query.filter_by(public_id=movie).first()
    io.emit("Watch", {
        "host": host,
        "movie": movie_.movies,
        'room': active.unique_id
    }, room=active.unique_id, broacast=True)



@io.on('paused')
def paused(data):
    room = data['room_id']
    movie = data['movie_id']
    current_time = data['paused_time']
    active = Room.query.filter_by(unique_id=room).first()
    r_activity = Room_Activities.query.filter_by(activity=active).filter_by(movie=movie).first()
    if r_activity:
        r_activity.vid_time = current_time
        db.session.commit()
        io.emit('Pause_time', f'Movie paused at {current_time}')
        io.emit("Continuation", {
            "host": active.host,
            "movie": movie,
            'room': active.unique_id,
            "current_time": r_activity.vid_time
        }, room=active.unique_id, broadcast=True)
    else:
        pass


# send message
@io.on("group_message")
def on_new_message(message):
    room = message['room']
    print(str(message))
    active = Room.query.filter_by(unique_id=room).first()
    if not active:
        io.emit('New_group_Message', {'message': f'New message from {message["name"]}'}, broadcast=True)
        io.emit("New", {
            "sender": message['name'],
            "time": datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
            "data": message['message'],
        },  broadcast=True)
    else:
        io.emit('New_group_Message', {'message': f'Room not found'})



@io.on('disconnect')
def disconnect():
    io.emit("disconnected",
         {"message": 'Disconnected'})


@io.on_error(namespace='/room')
def chat_error_handler(e):
    print('An error has occurred: ' + str(e))


@io.on('online')
def online(data):
    io.emit('status_change', {'username': data['name'], 'status': 'online'}, broadcast=True)



@io.on("offline")
def offline(data):
    active = []
    friends = Friend.query.filter_by(get=current_user).all()
    friend_schema = FriendSchema(many=True)
    result = friend_schema.dump(friends)
    for value in result:
        for i, v in value.items():
            if i == 'u_friend':
                active.append(v)
    for f in active:
        if data['data'] in f:
            online_friend.remove(f)
    emit('status_change', {'username': online_friend, 'status': 'offline'}, broadcast=True)


@io.on("video_chat", namespace='/chat')
def on_video_chat(data):
    room = data['room']
    active = Room.query.filter_by(unique_id=room).first()


@io.on('vote')
def handleVote(ballot):
    vote = Vote(votes=ballot)
    db.session.add(vote)
    db.session.commit()

    result1 = Vote.query.filter_by(votes=1).count()
    result2 = Vote.query.filter_by(votes=2).count()
    print(result1, result2)
    io.emit('vote_result', {'result1': result1, 'result2': result2}, broadcast=True)
