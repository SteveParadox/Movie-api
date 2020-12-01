import os


class Config:
    def __init__(self):
        pass

    ENV = 'prod'

    if ENV == 'dev':
        SECRET_KEY = 'os.environ.ge'
        API_KEY = os.environ.get('SECRET_KEY')
        SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        CORS_HEADERS = 'Content-Type'
    else:
        SECRET_KEY = "795849f0d2328258710ae9c71cb795849f0d2328258710ae9c71cb4b5ea4b5ea"
        API_KEY = "795849f0d2328258710ae9c71cb4b5ea"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_DATABASE_URI = "postgres://tmezmgejayycxt:96acdc27bfed485a4d2b4533ac7455e2985763907c71a171edf79a9529c8e3a8@ec2-34-202-65-210.compute-1.amazonaws.com:5432/dbgri8ojt9m5pe"
        CORS_HEADERS = 'Content-Type'
