from flask import Flask
from flask_login import current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

from views import *


if __name__ == '__main__':
    app.run()
