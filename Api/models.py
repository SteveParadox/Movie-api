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
    country = db.Column(db.String())
    phone_no = db.Column(db.String())
    password = db.Column(db.String(), nullable=False)
    logged_in = db.Column(db.Boolean, default=False)
    pair = db.Column(db.String())
    friends = db.relationship('Friend', backref='get', lazy=True)
    my_movies = db.relationship('Data', backref='love', lazy=True)
    loved = db.relationship('Exciting', backref='rate', lazy=True)
    activity = db.relationship('Activities', backref='social', lazy=True)
    save_ = db.relationship('Store', backref='saved', lazy=True)
    admin = db.Column(db.Boolean, default=False)
    review_ = db.relationship('userRating', backref='reviews', lazy=True)
    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    review = db.Column(db.Float)
    runtime = db.Column(db.Float)
    created_on = db.Column(db.String())
    creator = db.Column(db.String())
    cast1 = db.Column(db.String())
    cast2 = db.Column(db.String())
    cast3 = db.Column(db.String())
    cast4 = db.Column(db.String())
    genre = db.Column(db.JSON)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    thumbs_up = db.Column(db.Integer, default=0)
    thumbs_down = db.Column(db.Integer, default=0)
    popular = db.Column(db.Integer, default=0)
    reviewed_ = db.relationship('userRating', backref='reviewing', lazy=True)

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    overview = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Float)
    runtime = db.Column(db.Integer)
    total_seasons = db.Column(db.Integer)
    first_aired_on = db.Column(db.String())
    languages = db.Column(db.JSON)
    production_companies = db.Column(db.JSON)
    kind = db.Column(db.String())
    series_years = db.Column(db.String())
    genre = db.Column(db.JSON)  # , dimensions=1))
    sound_mix = db.Column(db.String())
    aspect_ratio = db.Column(db.String())
    thumbs_up = db.Column(db.Integer, default=0)
    thumbs_down = db.Column(db.Integer, default=0)
    season_list = db.relationship('Series_Season', backref='season', lazy=True)


class Series_Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer)
    episode = db.Column(db.String())
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    ep_list = db.relationship('Series_Episodes', backref='episodes', lazy=True)


class Series_Episodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episode_name = db.Column(db.String())
    overview = db.Column(db.String())
    movies = db.Column(db.String)
    movie_data = db.Column(db.LargeBinary)
    episode_no = db.Column(db.Integer)
    poster = db.Column(db.String)
    poster_data = db.Column(db.LargeBinary)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    thumbs_up = db.Column(db.Integer, default=0)
    thumbs_down = db.Column(db.Integer, default=0)
    series_season_id = db.Column(db.Integer, db.ForeignKey('series__season.id'))


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    u_friend = db.Column(db.String())

    def __repr__(self):
        return f"Friend('{self.u_friend}')"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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
    adventure = db.Column(db.Boolean, default=False)
    children = db.Column(db.Boolean, default=False)
    family = db.Column(db.Boolean, default=False)
    crime = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Data('{self.user_id}')"


class Exciting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loved = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story = db.Column(db.String(50))
    story_data = db.Column(db.LargeBinary)
    time_uploaded = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stored_data = db.Column(db.String(100))
    time_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class userRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    time_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))



class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    votes = db.Column('data', db.Integer, default=0)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(), unique=True, nullable=False)
    host = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    r_activity = db.relationship('Room_Activities', backref='activity', lazy=True)

    def __repr__(self):
        return f"Room('{self.unique_id}', '{self.host}', '{self.admin}')"


class Room_Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie = db.Column(db.String())
    vid_time = db.Column(db.String())
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


class FriendSchema(ModelSchema):
    class Meta:
        model = Friend


friend_schema = FriendSchema
friends_schema = FriendSchema(many=True)




class StoreSchema(ModelSchema):
    class Meta:
        model = Store


store_schema = StoreSchema
stores_schema = StoreSchema(many=True)


class ExcitingSchema(ModelSchema):
    class Meta:
        model = Exciting


exciting_schema = ExcitingSchema
excitings_schema = ExcitingSchema(many=True)


class ActivitiesSchema(ModelSchema):
    class Meta:
        model = Activities


activities_schema = ActivitiesSchema
activitiess_schema = ActivitiesSchema(many=True)


class DataSchema(ModelSchema):
    class Meta:
        model = Data


data_schema = DataSchema
data_schemas = DataSchema(many=True)


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


class SeriesSchema(ModelSchema):
    class Meta:
        model = Series


serie_schema = SeriesSchema
series_schema = SeriesSchema(many=True)


class Series_SeasonSchema(ModelSchema):
    class Meta:
        model = Series_Season


serie_season_schema = Series_SeasonSchema
series_season_schema = Series_SeasonSchema(many=True)
