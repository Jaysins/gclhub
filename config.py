import os

file_path = os.path.abspath(os.getcwd()) + "\service.db"

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'thisisasecret'
