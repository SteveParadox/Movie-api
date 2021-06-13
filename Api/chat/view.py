import uuid
from flask import *
from flask_cors import cross_origin
from flask_login import current_user, login_required
from flask_socketio import emit, close_room, leave_room, join_room

from Api import *
from Api.models import Room, RoomSchema, Users, Friend, FriendSchema, Movie, Vote, Room_Activities, UsersSchema
from Api.ext import token_required

chat = Blueprint('chat', __name__)

store = []
online_friend = []


# all users
@chat.route('/api/friends/you/may/know')
def friendsYouMayKnow():
    pair = Users.query.all()
    users_schema = UsersSchema(many=True)
    result = users_schema.dump(pair)
    return jsonify(result)

# adding a friend to watch with
@chat.route('/api/add/friend/<string:name>', methods=["GET", 'POST'])
@cross_origin()
@token_required
def add(current_user, name):
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
@token_required
def remove_(current_user, name):
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
@chat.route('/api/my/friends', methods=['POST'])
@cross_origin()
@token_required
def my_friends(current_user):
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
@token_required
def create_room(current_user, movie):
    try:
        created_room = str(uuid.uuid4())
        movie = Movie.query.filter_by(public_id=movie).first()
        host = current_user.name
        room = Room()
        room.unique_id = created_room
        room.host = host
        room.admin = True
        db.session.add(room)
        db.session.commit()

        return jsonify(
            {
                "message": f"Room {created_room} created by {host} ",
                
                "movie name": movie.name
            }
        )
    except:
        return jsonify({
            "message": "Cannot find movie id"
        })

    

# redirecting to the room id
@chat.route('/api/watch/<string:movie_id>/in/room/<string:room>', methods=['GET'])
@cross_origin()
def watch(movie_id, room):
    movie = Movie.query.filter_by(public_id=movie_id).first()
    room = Room.query.filter_by(unique_id=room).first()
    if room:

        store.append(room.unique_id)
        return jsonify(
            {
                "movie name": movie.name,
                'room': room.unique_id,
                
            }
        )
    else:
        return jsonify({
            'message': 'Error... not found'
        }), 404



@chat.route('/api/my/rooms', methods=['GET'])
@cross_origin()
@token_required
def my_rooms(current_user):
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
@token_required
def delete_room(current_user, room_id):
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
    io.to(request.sid).emit('resp', {'message': 'connected', 'your_id': request.sid}, room=request.sid)

@io.on("disconnect")
def on_disconnect():
    io.emit('callEnded', {'message': 'call ended'}, broadcast = True )


@io.on('callUser')
def call(data):
    payload = {'signal': data['signalData'], 'from': data['from'], 'to': data['to'], 'name':data['name'], 'status': 'joined'}
    io.to(data.userToCall).emit('callUser', payload, room=data.userToCall, broadcast=True)  


@io.on('callAccepted')
def callAccepted(data):
    io.to(data.to).emit('callAccepted', {'signal': data['signal']}, room=data.to, broadcast=True)


@io.on('online')
def online(data):
    friend = Friend.query.filter_by(get=current_user).filter_by(u_friend=data['name']).first()

    if friend:
        print(friend.u_friend)
        io.emit('status_change', {'username': data['name'], 'status': 'online'}, broadcast=True)
    elif current_user.name == data['name']:
        print(current_user.name)
        io.emit('status_change', {'username': data['name'], 'status': 'online'}, broadcast=True)

    else:
        pass


# joining room
@io.on("join_user")
def on_new_user(data):
    room = data['room_id']
    active_ = Room.query.filter_by(unique_id=room).first()
    join_room(active_.unique_id)


@io.on('joined')
def joined_room(data):
    room = data['room_id']
    active = Room.query.filter_by(unique_id=room).first()
    io.emit('joined_room', {'username': data['name'], 'room': active.unique_id, 'status': 'joined'},
            room=active.unique_id, broadcast=True)


# send message to joined room
@io.on("group_message")
def on_new_message(message):
    room = message['room_id']
    print(str(message))
    active = Room.query.filter_by(unique_id=room).first()
    if active:
        io.emit('New_group_Message', {'message': f'New message from {message["name"]}'}, room=active.unique_id,
                broadcast=True)
        io.emit("New", {
            "sender": message['name'],
            "time": datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
            "data": message['message'],
        }, room=active.unique_id, broadcast=True)
    else:
        io.emit('New_group_Message', {'message': f'Room not found'})


# leave room
@io.on("leave_room")
def on_leave_room(data):
    room = data['room_id']
    name = data['name']
    active = Room.query.filter_by(unique_id=room).first()
    leave_room(active.unique_id)
    if name == active.host:
        close_room(active.unique_id)
        db.session.delete(active.unique_id)
        return redirect(url_for("api.home"))
    io.emit("Left_user", {"message": f"{name} has left the room"}, room=active.unique_id, broadcast=True)


# close room
@io.on("close_room")
def on_close_room(data):
    room = data['data']
    active = Room.query.filter_by(host=current_user.name) \
        .filter_by(admin=True) \
        .filter_by(unique_id=room).first()
    io.close_room(active.unique_id)
    db.session.delete(active.unique_id)
    return redirect(url_for("api.home"))


# watch movie
@io.on('watch_movie')
def on_video_stream(data):
    room = data['room_id']
    movie = data['movie_id']
    active = Room.query.filter_by(unique_id=room).first()
    movies = Movie.query.filter_by(public_id=movie).first()
    r_activities = Room_Activities(activity=active)
    r_activities.movie = movies.name
    db.session.add(r_activities)
    db.session.commit()
    host = active.host
    r_activities = Room_Activities.query.filter_by(activity=active).first()

    io.emit("Watch", {
        "host": host,
        'movie_id': movie,
        'room_id': room,
        'time': r_activities.vid_time
    }, room=active.unique_id, broacast=True)


@io.on('send_invite')
def invite(data):

    io.emit('Invited', {"data": data}, broadcast=True)


@io.on('get_time')
def get_time_(data):
    room = data['room_id']
    movie = data['movie_id']
    active = Room.query.filter_by(unique_id=room).first()
    movies = Movie.query.filter_by(public_id=movie).first()
    r_activities = Room_Activities(activity=active)
    r_activities.movie = movies.name
    print(f"time is {data['current_time']}")
    r_activities.vid_time = data['current_time']
    db.session.commit()
    print(r_activities.vid_time)
    io.emit("Joined", {
        'movie_id': movie,
        'room_id': room,
        'time': r_activities.vid_time
    }, room=active.unique_id, broacast=True)


@io.on('paused_movie')
def paused_(data):
    room = data['room_id']
    active = Room.query.filter_by(unique_id=room).first()
    r_activity = Room_Activities.query.filter_by(activity=active).first()

    io.emit("Continuation", {
        'message': f" movie is paused"
    }, room=active.unique_id, broadcast=True)


@io.on('play_movie')
def play_(data):
    room = data['room_id']
    active = Room.query.filter_by(unique_id=room).first()
    r_activity = Room_Activities.query.filter_by(activity=active).first()

    print(room)
    io.emit("Continued", {
        'message': f" movie is playing"
    }, room=active.unique_id, broadcast=True)


@io.on('disconnect')
def disconnect():
    io.emit("disconnected",
            {"message": 'Disconnected'})


@io.on_error(namespace='/room')
def chat_error_handler(e):
    print('An error has occurred: ' + str(e))


@io.on("offline")
def offline(data):
    emit('status_offline', {'username': data['name'], 'status': 'offline'}, broadcast=True)


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
