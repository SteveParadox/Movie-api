
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, DateField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class Sign_Up(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    dob = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit ')


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit ')