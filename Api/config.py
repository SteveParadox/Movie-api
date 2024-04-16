import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    def __init__(self):
        pass

    ENV = os.getenv('ENV')

    if ENV == 'dev':
        SECRET_KEY = os.getenv('SECRET_KEY')
        API_KEY = os.getenv('API_KEY')
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        CORS_HEADERS = 'Content-Type'
    else:
        SECRET_KEY = os.getenv('SECRET_KEY')
        API_KEY = os.getenv('API_KEY')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
        CORS_HEADERS = 'Content-Type'
