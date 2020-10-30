import datetime
from flask import *
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS()
app.config.from_object(Config)
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login_users'
login_manager.login_message = None
login_manager.session_protection = "strong"
REMEMBER_COOKIE_NAME= 'remember_token'
REMEMBER_COOKIE_DURATION=datetime.timedelta(days=64, seconds=29156, microseconds=10)
REMEMBER_COOKIE_REFRESH_EACH_REQUEST=False


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)
   # mail.init_app(app)
    # socketio.init_app(app)
    #jwt.init_app(app)
    from .api.routes import api
    from .users.routes import users
    from .upload.routes import upload

    app.register_blueprint(api)
    app.register_blueprint(users)
    app.register_blueprint(upload)

    return app
