import datetime
import flask
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from flask_cors import CORS
from flask_socketio import SocketIO
#from flask_jwt_extended import JWTManager

app = Flask(__name__)
cors = CORS()
io = SocketIO()
#jwt= JWTManager()


app.config.from_object(Config)

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = None
io.manage_session= False
login_manager.session_protection = "strong"
REMEMBER_COOKIE_NAME = 'remember'
REMEMBER_COOKIE_DURATION = datetime.timedelta(days=64, seconds=29156, microseconds=10)
REMEMBER_COOKIE_REFRESH_EACH_REQUEST = True


@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=200000000)
    flask.session.modified = True

   

def create_app(config_class=Config):

    db.init_app(app)
    io.init_app(app, cors_allowed_origins="*")
    bcrypt.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    #jwt.init_app(app)
  
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

'''@app.after_request
    def after_request_func(response):
        origin = request.headers.get('Origin')
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
            response.headers.add('Access-Control-Allow-Methods',
                                'GET, POST, OPTIONS, PUT, PATCH, DELETE')
            if origin:
                response.headers.add('Access-Control-Allow-Origin', origin)
        else:
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            if origin:
                response.headers.add('Access-Control-Allow-Origin', origin)

        return response

'''

