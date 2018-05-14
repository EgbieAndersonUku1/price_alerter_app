from functools import wraps
from flask import redirect, url_for, request

from utils.security.sessions import Session
from app import app


def login_required(f):

    @wraps(f)
    def login(*args, **kwargs):
        if not Session.lookup('email'):
            return redirect(url_for('login_app.login', next=request.path))
        return f(*args, **kwargs)
    return login


def is_user_already_logged_in(f):
    @wraps(f)
    def logged_in(*args, **kwargs):
        if Session.lookup('login_token'):
            return redirect(url_for('home_page_app.home_page'))
        return f(*args, **kwargs)
    return logged_in


