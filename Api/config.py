import os


class Config:
    def __init__(self):
        pass

    ENV = 'prod'

    if ENV == 'dev':
        SECRET_KEY = os.environ.get('SECRET_KEY')
        API_KEY = os.environ.get('SECRET_KEY')
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    else:
        SECRET_KEY = "795849f0d2328258710ae9c71cb4b5ea"
        API_KEY = "795849f0d2328258710ae9c71cb4b5ea"
        SQLALCHEMY_DATABASE_URI = 'postgres://ufiptzttzuntox:387caedfd883109ecc8be4445c7f6b8d24ade865c271a07d804ccba4d92a5be6@ec2-54-160-161-214.compute-1.amazonaws.com:5432/d4avvp9u9sf1n5'


