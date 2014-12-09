__author__ = 'hansihe'

from flask import render_template, abort
from flask.ext.classy import FlaskView
from sqlalchemy.orm.exc import NoResultFound
from models.board import Board
from models.thread import Thread
from models.post import Post
from . import blueprint
from ext import db


class BoardView(FlaskView):
    def get(self, text_id):
        try:
            board = Board.get_board_by_text_id(text_id)
        except NoResultFound:
            return abort(404)

        threads = db.session.query(Thread, Post)\
            .filter_by(board_id=board.id)\
            .order_by(Thread.id.desc())\
            .join(Post, Thread.id == Post.thread_id)\
            .all()

        print(db.session.query(Thread, Post)
              .filter_by(board_id=board.id)
              .order_by(Thread.id.desc())
              .join(Post, Thread.id == Post.thread_id).statement)

        for thread in threads:
            print(thread.__dict__)

        return render_template("forum_threads_view.jinja2", board=board, title=board.name, can_post=True, threads=threads)

BoardView.register(blueprint)