__author__ = 'hansihe'

from flask import render_template, abort
from flask.ext.classy import FlaskView
from sqlalchemy.orm.exc import NoResultFound
from models.board import Board
from models.thread import Thread
from . import blueprint


class BoardView(FlaskView):
    def get(self, text_id):
        try:
            board = Board.get_board_by_text_id(text_id)
        except NoResultFound:
            return abort(404)

        threads = Thread.query.filter_by(board_id=board.id).order_by(Thread.id.desc()).all()

        return render_template("forum_threads_view.jinja2", board=board, title=board.name, can_post=True, threads=threads)

BoardView.register(blueprint)