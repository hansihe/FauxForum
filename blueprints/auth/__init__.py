__author__ = 'hansihe'

from flask import Blueprint
from ext import login
from models.user import User

blueprint = Blueprint("auth", "auth")

@login.user_loader
def load_user(user_id):
    try:
        return User.get_user_by_id(int(user_id))
    except ValueError:
        return None

import register, login