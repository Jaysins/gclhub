# coding=utf-8

"""
APP.py
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)

app.config.from_pyfile('config.py')

mail = Mail(app)


s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

# noinspection PyUnresolvedReferences
from views import *


if __name__ == '__main__':    
    # app.run(host='192.168.1.24')
    app.run(port='8080')
