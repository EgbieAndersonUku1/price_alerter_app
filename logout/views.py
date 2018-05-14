from flask import Blueprint, redirect, url_for

from utils.security.sessions import Session

logout_app = Blueprint('logout_app', __name__, url_prefix='/logout')


@logout_app.route('/')
def logout():
    """Logs the user out of the application"""

    Session.delete_login_credentials()
    return redirect(url_for('login_app.login'))