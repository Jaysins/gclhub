import os

file_path = os.path.abspath(os.getcwd()) + "\service.db"

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'thisisasecret'
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
