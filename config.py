from dotenv import load_dotenv
load_dotenv(verbose=True)
#basedir = os.path.abspath(os.path.dirname(__file__))
import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'