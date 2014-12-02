__author__ = 'hansihe'

from models import board
from util import full_date


def init(app):

    def get_boards():
        boards = board.Board.query.filter_by().all()
        return boards

    @app.context_processor
    def inject():
        return dict(get_boards=get_boards, getattr=getattr, full_date=full_date)