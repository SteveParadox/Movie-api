import datetime
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
cors = CORS()
io = SocketIO()

app.config.from_object(Config)

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()
try:
    login_manager.login_view = 'raw.login_users'
except:
    login_manager.login_view = 'users.login'
login_manager.login_message = None
io.manage_session= False
login_manager.session_protection = "strong"
REMEMBER_COOKIE_NAME = 'remember_token'
REMEMBER_COOKIE_DURATION = datetime.timedelta(days=64, seconds=29156, microseconds=10)
REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
  
    # mail.init_app(app)

    from .api.routes import api
    from .users.routes import users
    from .upload.routes import upload
    from .chat.view import chat
    from .raw.routes import raw

    app.register_blueprint(api)
    app.register_blueprint(raw)
    app.register_blueprint(users)
    app.register_blueprint(upload)
    app.register_blueprint(chat)

    return app
