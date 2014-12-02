__author__ = 'hansihe'

from ext import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    text = db.Column(db.Text(length=10000, convert_unicode=True))

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    thread = db.relationship('Thread', backref=db.backref('posts', lazy='dynamic', order_by=id), foreign_keys="Post.thread_id")

    op = db.Column(db.Boolean, default=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))

    creation_time = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, text, thread, author_id):
        self.text = text
        self.thread = thread
        self.author_id = author_id
        self.creation_time = datetime.utcnow()