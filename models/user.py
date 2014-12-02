__author__ = 'hansihe'

from ext import bcrypt, db
from flask.ext.login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    password_hash = db.Column(db.String(60))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password, rounds=12)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    def get_id(self):
        return unicode(self.id)