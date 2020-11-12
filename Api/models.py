from datetime import datetime

from flask_login import UserMixin

from marshmallow_sqlalchemy import ModelSchema

from . import db, login_manager


@login_manager.user_loader
def load_user(users_id):
    return Users.query.get(int(users_id))



class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    dob = db.Column(db.String())
    password = db.Column(db.String(), nullable=False)
    pair = db.Column(db.String())
    friends = db.relationship('Friend', backref='get', lazy=True)
    action = db.Column(db.Boolean, default=False)
    comedy = db.Column(db.Boolean, default=False)
    horror = db.Column(db.Boolean, default=False)
    documentary = db.Column(db.Boolean, default=False)
    mystery = db.Column(db.Boolean, default=False)
    animation = db.Column(db.Boolean, default=False)
    sci_fi = db.Column(db.Boolean, default=False)
    romance = db.Column(db.Boolean, default=False)
    erotic = db.Column(db.Boolean, default=False)
    fantasy = db.Column(db.Boolean, default=False)
    drama = db.Column(db.Boolean, default=False)
    thriller = db.Column(db.Boolean, default=False)
    para_normal = db.Column(db.Boolean, default=False)
    family = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    review = db.Column(db.Float)
    movies = db.Column(db.String)
    movie_data = db.Column(db.LargeBinary)
    poster = db.Column(db.String)
    poster_data = db.Column(db.LargeBinary)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    thumbs_up = db.Column(db.Integer, default=0)
    thumbs_down = db.Column(db.Integer, default=0)
    admin = db.Column(db.Boolean, default=False)





class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    u_friend = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Friend('{self.u_friend}')"


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(), unique=True, nullable=False)
    host = db.Column(db.String(), nullable=False)
    vid_time = db.Column(db.String())
    admin = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Room('{self.unique_id}', '{self.host}', '{self.admin}')"


class FriendSchema(ModelSchema):
    class Meta:
        model = Friend


friend_schema = FriendSchema
friends_schema = FriendSchema(many=True)


class MovieSchema(ModelSchema):
    class Meta:
        model = Movie


movie_schema = MovieSchema
movies_schema = MovieSchema(many=True)


class RoomSchema(ModelSchema):
    class Meta:
        model = Room


room_schema = RoomSchema
rooms_schema = RoomSchema(many=True)


class UsersSchema(ModelSchema):
    class Meta:
        model = Users


user_schema = UsersSchema
users_schema = UsersSchema(many=True)
