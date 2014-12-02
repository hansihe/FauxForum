__author__ = 'hansihe'

from . import blueprint
from flask.ext.classy import FlaskView
from flask import render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Length, EqualTo

from models.user import User
from ext import db


class UsernameNotUsedValidator():
    def __init__(self, message="This username is already taken."):
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError(message=self.message)


class RegisterForm(Form):
    username = StringField("Username", [
        InputRequired(message="Please enter a username."),
        Length(min=3, max=16, message="Usernames must be between 3 and 16 characters."),
        UsernameNotUsedValidator()])

    password = PasswordField("Password", [
        InputRequired(message="Please enter a password."),
        Length(min=8, message="The password must be over 8 characters long.")])
    confirm_password = PasswordField("Confirm Password", [
        InputRequired(message="Please enter your password again."),
        EqualTo('password', message="Passwords are not equal.")])

    submit = SubmitField()


class RegisterView(FlaskView):
    def index(self):
        form = RegisterForm()
        return render_template("register.jinja2", form=form, getattr=getattr)

    def post(self):
        form = RegisterForm()

        if form.validate():
            user = User(username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()

            flash("Registration successful. You can now log in.")
            return redirect(url_for("auth.LoginView:index"))

        return render_template("register.jinja2", form=form, getattr=getattr)

RegisterView.register(blueprint)