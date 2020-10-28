from datetime import datetime

from flask_login import UserMixin

from marshmallow_sqlalchemy import ModelSchema

from . import db, login_manager



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), default=0)
    description = db.Column(db.String(), nullable=False)
    review = db.Column(db.Float)
    movies = db.Column(db.String)
    genre = db.Column(db.String)
    movie_data = db.Column(db.LargeBinary)
    poster = db.Column(db.String)
    poster_data = db.Column(db.LargeBinary)
    date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.now)
    

    
class Users(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  email = db.Column(db.String())
  dob = db.Column(db.String())
  password = db.Column(db.String())
  vid_time= db.Column(db.String())
  pair= db.Column(db.String())
  
  
  def __repr__(self):
        return f"User('{self.name}', '{self.email}')"
  
      
  
class MovieSchema(ModelSchema):
    class Meta:
        model = Movie


movie_schema = MovieSchema
movies_schema = MovieSchema(many=True)



class UsersSchema(ModelSchema):
    class Meta:
        model = Users


user_schema = UsersSchema
users_schema = UsersSchema(many=True)
