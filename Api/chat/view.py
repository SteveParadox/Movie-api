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
    movie = Movie.query.filter_by(public_id=movie).first()
    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    created_room = str(uuid.uuid4())
    host = current_user.name
    room = Room(unique_id=created_room, host=host, admin=True)

    db.session.add(room)
    db.session.commit()

    return jsonify({
        "message": f"Room {created_room} created by {host}",
        "movie name": movie.name
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
    io.to(request.namespace.socket.sessid).emit('resp', {'message': 'connected', 'your_id': request.namespace.socket.sessid}, room=request.namespace.socket.sessid)

@io.on("disconnect")
def on_disconnect():
    io.emit('callEnded', {'message': 'call ended'}, broadcast = True )


@io.on('callUser')
def call(data):
    room = Room.query.filter_by(unique_id=data['room']).first()
    if room:
        io.to(data['userToCall']).emit('callUser', {
            'signal': data['signalData'],
            'from': data['from'],
            'to': data['to'],
            'name': data['name'],
            'room': room.unique_id,
            'status': 'joined'
        }, room=room.unique_id, broadcast=True)
    else:
        io.emit('userError', {'message': 'Room not found'}, room=request.sid)


@io.on('answerCall')
def answerCall(data):
    io.to(data.to).emit('callAccepted', {'signal': data['signal'],
     'room': active.unique_id},
            room=active.unique_id, broadcast=True)


@io.on('online')
def online(data):
    try:
        friend = Friend.query.filter_by(get=current_user).filter_by(u_friend=data['name']).first()
        
        if friend:
            print(friend.u_friend)
            io.emit('status_change', {'username': data['name'], 'status': 'online'}, broadcast=True)
        elif current_user.name == data['name']:
            print(current_user.name)
            io.emit('status_change', {'username': data['name'], 'status': 'online'}, broadcast=True)
        else:
            pass
    except Exception as e:
        print(f"Error in 'online' function: {e}")
        io.emit('error', {'message': f"An error occurred while processing your request: {str(e)}"}, broadcast=True)



# joining room
@io.on("join_user")
def on_new_user(data):
    room = Room.query.filter_by(unique_id=data['room_id']).first()
    join_room(room.unique_id)



@io.on('joined')
def joined_room(data):
    room_id = data.get('room_id')
    name = data.get('name')

    if not room_id:
        return

    active = Room.query.filter_by(unique_id=room_id).first()

    if not active:
        return

    join_room(active.unique_id)

    io.emit('joined_room', {
        'username': name, 
        'room': active.unique_id, 
        'status': 'joined'
    }, room=active.unique_id)



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
  
@io.on('private_message')
def on_private_message(data):
    recipient_name = data['to']
    sender_name = data['from']
    message = data['message']
    
    # Look up recipient and sender users
    recipient = User.query.filter_by(name=recipient_name).first()
    sender = User.query.filter_by(name=sender_name).first()
    
    if recipient and sender:
        # Emit private message to recipient
        io.emit('new_private_message', {'sender': sender_name, 'message': message}, room=recipient.sid)
        
        # Emit confirmation message to sender
        io.emit('private_message_sent', {'recipient': recipient_name, 'message': message})
    else:
        io.emit('private_message_error', {'message': 'Recipient or sender not found'})



# leave room
@io.on("leave_room")
def on_leave_room(data):
    room = data['room_id']
    name = data['name']
    active = Room.query.filter_by(unique_id=room).first()
    leave_room(active.unique_id)
    
    if name == active.host:
        close_room(active.unique_id)
        db.session.delete(active)
        db.session.commit()
        return redirect(url_for("api.home"))
    
    io.to(active.unique_id).emit("user_left_room", {"username": name, "message": f"{name} has left the room"})


# close room
@io.on("close_room")
def on_close_room(data):
    room_id = data.get("room_id")
    active_room = Room.query.filter_by(unique_id=room_id, host=current_user.name, admin=True).first()
    if not active_room:
        return jsonify({"error": "You are not authorized to close this room."})
    
    io.close_room(room_id)
    db.session.delete(active_room)
    db.session.commit()
    
    return jsonify({"message": "Room closed successfully."})



# watch movie
@io.on('watch_movie')
def on_watch_movie(data):
    room = data['room_id']
    movie = data['movie_id']
    active = Room.query.filter_by(unique_id=room).first()
    movies = Movie.query.filter_by(public_id=movie).first()

    if active and movies:
        r_activities = Room_Activities(activity=active)
        r_activities.movie = movies.name
        db.session.add(r_activities)
        db.session.commit()
        
    r_activities.movie = movie.name
    r_activities.vid_time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    db.session.commit()

    host = active_room.host

    # Emit an event to all clients in the room with the movie information and current timestamp
    io.emit('Watch', {
        'host': host,
        'movie_id': movie_id,
        'movie_name': movie.name,
        'room_id': room_id,
        'time': r_activities.vid_time
    }, room=active_room.unique_id, broadcast=True)


@io.on('send_invite')
def send_invite(invite):
    room_id = invite.get('room_id')
    username = invite.get('username')
    room = Room.query.filter_by(unique_id=room_id).first()
    if room:
        invite_data = {
            'room_id': room_id,
            'room_name': room.name,
            'inviter': current_user.name
        }
        io.emit('invitation', invite_data, room=room_id, include_self=False)
        flash(f'Invitation sent to {username} for {room.name}')
    else:
        flash(f'Room with id {room_id} does not exist')



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
    room_id = data.get('room_id')
    if not room_id:
        return

    active_room = Room.query.filter_by(unique_id=room_id).first()
    if not active_room:
        io.emit('Error', {'message': 'Room not found'}, room=request.sid)
        return

    room_activities = Room_Activities.query.filter_by(activity=active_room).first()
    if not room_activities:
        io.emit('Error', {'message': 'Room activities not found'}, room=request.sid)
        return

    room_activities.paused = True
    room_activities.last_played_time = datetime.now()
    db.session.commit()

    io.emit("Continuation", {
        'message': f"Movie is paused",
        'paused_time': room_activities.last_played_time.timestamp()
    }, room=active_room.unique_id, broadcast=True)



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
    room_id = data.get('room_id')
    username = data.get('username')

    if not room_id or not username:
        return

    # Get the active room
    active_room = Room.query.filter_by(unique_id=room_id).first()

    if not active_room:
        return

    # Broadcast the event to the room
    io.emit("new_video_chat", {
        "room_id": room_id,
        "username": username,
        "message": f"{username} started a video chat"
    }, room=active_room.unique_id, broadcast=True)



@io.on('vote')
def handleVote(ballot):
    vote = Vote(votes=ballot)
    db.session.add(vote)
    db.session.commit()

    result1 = Vote.query.filter_by(votes=1).count()
    result2 = Vote.query.filter_by(votes=2).count()
    print(result1, result2)
    io.emit('vote_result', {'result1': result1, 'result2': result2}, broadcast=True)
