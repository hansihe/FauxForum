__author__ = 'hansihe'

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()


def init(app):
    db.app = app
    db.init_app(app)

    bcrypt.init_app(app)

    login.init_app(app)