__author__ = 'hansihe'

from ext import db
from datetime import datetime


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(60), nullable=False)

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship('Board', backref=db.backref('posts', lazy='dynamic'))

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('threads', lazy='dynamic'))

    creation_time = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, title, board_id, author_id):
        self.title = title
        self.board_id = board_id
        self.author_id = author_id
        self.creation_time = datetime.utcnow()