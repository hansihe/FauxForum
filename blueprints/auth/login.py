__author__ = 'hansihe'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask.ext.classy import FlaskView
from flask import render_template, flash, redirect, url_for
from models.user import User
from flask_login import login_user, logout_user
from . import blueprint


class LoginForm(Form):
    username = StringField("Username", [
        InputRequired(message="Please enter a username.")])
    password = PasswordField("Password", [
        InputRequired(message="Please enter a password.")])

    submit = SubmitField()


class LoginView(FlaskView):
    def index(self):
        form = LoginForm()
        return render_template("login.jinja2", form=form, getattr=getattr)

    def post(self):
        form = LoginForm()

        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()

            if user is None or not user.verify_password(form.password.data):
                flash("Wrong username or password", "alert")
                return render_template("login.jinja2", form=form, getattr=getattr)

            login_user(user)

            flash("You are now logged in.")
            return redirect(url_for("index"))

        return render_template("login.jinja2", form=form, getattr=getattr)

LoginView.register(blueprint)


@blueprint.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))