import os


class Config:
    def __init__(self):
        pass

    ENV = 'dev'

    if ENV == 'dev':
        SECRET_KEY = os.environ.get('SECRET_KEY')
        API_KEY = os.environ.get('SECRET_KEY')
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        SECRET_KEY = "795849f0d2328258710ae9c71cb4b5ea"
        API_KEY = "795849f0d2328258710ae9c71cb4b5ea"
        SQLALCHEMY_DATABASE_URI = ''


