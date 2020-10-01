from datetime import datetime

from marshmallow_sqlalchemy import ModelSchema

from . import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(), nullable=False)
    name = db.Column(db.Integer, default=0)
    description = db.Column(db.String(), nullable=False)
    review = db.Column(db.Integer, default=0)
    movies = db.Column(db.String)
    movie_data = db.Column(db.LargeBinary)
    poster = db.Column(db.String)
    poster_data = db.Column(db.LargeBinary)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)


class MovieSchema(ModelSchema):
    class Meta:
        model = Movie


movie_schema = MovieSchema
movies_schema = MovieSchema(many=True)
