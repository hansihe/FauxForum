__author__ = 'hansihe'

from flask import render_template, abort, redirect, url_for
from . import blueprint
from flask.ext.classy import FlaskView
from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import InputRequired, Length
from flask.ext.login import login_required
from flask.ext.classy import route as classy_route
from models.thread import Thread
from models.board import Board
from models.post import Post
from sqlalchemy.orm.exc import NoResultFound
from ext import db
from flask.ext.login import current_user


class ThreadPostForm(Form):
    title = StringField("Title", validators=[
        InputRequired(message="Please enter a title."),
        Length(min=3, max=60, message="A title must be between 3 and 60 characters.")])
    content = TextAreaField("Body", validators=[
        Length(max=10000, message="The body must be below 10000 characters long. (Really guy? 10000 characters? Wow)")])

    submit = SubmitField("Post thread")


class ThreadReplyForm(Form):
    content = TextAreaField("Body", validators=[
        Length(max=10000, message="The body must be below 10000 characters long. (Really guy? 10000 characters? Wow)")])

    submit = SubmitField("Post reply")


class ThreadPostView(FlaskView):
    route_base = "/board/<string:board_text_id>/post/"
    decorators = [login_required]

    def get(self, board_text_id):
        try:
            board = Board.get_board_by_text_id(board_text_id)
        except NoResultFound:
            return abort(404)

        form = ThreadPostForm()

        return render_template("forum_thread_post.jinja2", board=board, form=form)

    def post(self, board_text_id):
        try:
            board = Board.get_board_by_text_id(board_text_id)
        except NoResultFound:
            return abort(404)

        form = ThreadPostForm()
        if form.validate():
            thread = Thread(form.title.data, board.id, current_user.id)
            db.session.add(thread)
            db.session.commit()

            post = Post(form.content.data, thread, current_user.id)
            post.op = True
            db.session.add(post)
            db.session.commit()

        return render_template("forum_thread_post.jinja2", board=board, form=form)

ThreadPostView.register(blueprint)


class ThreadView(FlaskView):
    route_base = "/thread/<int:thread_id>"

    @classy_route('/', defaults={'page': 1})
    @classy_route('/page/<int:page>')
    def get(self, thread_id, page):
        try:
            thread = Thread.query.filter_by(id=thread_id).one()
        except NoResultFound:
            abort(404)

        posts_pagination = thread.posts.paginate(page, 20)
        posts = posts_pagination.items

        return render_template("forum_thread_view.jinja2", thread=thread, posts=posts,
                               posts_pagination=posts_pagination, board=thread.board,
                               reply_form=ThreadReplyForm())

    @classy_route('/post')
    def post(self):
        pass

ThreadView.register(blueprint)


class ThreadReplyView(FlaskView):
    route_base = "/thread/<int:thread_id>/reply"
    decorators = [login_required]

    def get(self, thread_id):
        try:
            thread = Thread.query.filter_by(id=thread_id).one()
        except NoResultFound:
            abort(404)
        form = ThreadReplyForm()

        return render_template("forum_thread_reply.jinja2", form=form, thread=thread)

    def post(self, thread_id):
        try:
            thread = Thread.query.filter_by(id=thread_id).one()
        except NoResultFound:
            abort(404)
        form = ThreadReplyForm()

        if form.validate():
            post = Post(form.content.data, thread, current_user.id)
            post.op = False

            db.session.add(post)
            db.session.commit()

            return redirect(url_for("forum.ThreadView:get_0", thread_id=thread_id, page=1))  # TODO: Redirect to last page of thread

        return render_template("forum_thread_reply.jinja2", form=form, thread=thread)

ThreadReplyView.register(blueprint)