__author__ = 'hansihe'

from ext import db


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text_id = db.Column(db.String(60), unique=True, nullable=False)
    name = db.Column(db.String(60), nullable=False)

    @classmethod
    def get_board_by_text_id(cls, text_id):
        return cls.query.filter_by(text_id=text_id).one()