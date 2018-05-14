from flask import url_for, redirect, Blueprint, render_template, request

from login.form import LoginForm
from users.models.user import User
from utils.decorators import is_user_already_logged_in

login_app = Blueprint('login_app', __name__, url_prefix='/login')


@login_app.route('/', methods=['GET', 'POST'])
@is_user_already_logged_in
def login():
    """Allows the user to login into the application"""

    form = _render_login_template()

    if request.method == 'POST' and form.validate_on_submit():

        user = User()
        account_status = user.Account.Retrieve.get_account_status(form.email.data)

        if account_status != 'ACCOUNT_CONFIRMED':
            return redirect(url_for(_get_status(account_status)))
        elif not user.Account.Login.is_login_valid(form.email.data, form.password.data):
            return redirect(url_for('login_app.no_user'))

        user.Account.Login.set_login_sessions(form.email.data)
        user.Account.Login.login()
        return redirect(url_for('home_page_app.home_page'))

    return render_template('login/login.html', form=form)


def _get_status(status):
    """_get_status(str) -> returns str


       There are three account status regarding the user.

       1) The first is the user has no account
       2) The second is the user has not confirmed their email
       3) The third is the user has confirmed their account.

       Depending on the account status redirects the user to the appropriate
       view function.
    """
    return {
        'ACCOUNT_NOT_FOUND': 'login_app.no_user',
        'EMAIL_NOT_CONFIRMED': 'login_app.login_confirm_email',
        'ACCOUNT_CONFIRMED': 'ACCOUNT_CONFIRMED'

    }.get(status)


@login_app.route('/incorrect', methods=['GET', 'POST'])
def no_user():
    """Redirects the user to this page if the user has an incorrect password or no account"""
    error = 'Incorrect username and password'
    return render_template('login/login.html', form=_render_login_template(), msg='', error=error)


@login_app.route('/confirm_email', methods=['GET', 'POST'])
def login_confirm_email():
    """Redirects the user here if the user has account but has not yet confirmed their email"""
    msg = 'You need to confirm your email'
    return render_template('login/login.html', form=_render_login_template(), msg=msg, error='')


def _render_login_template():
    """Renders the login template page"""
    return LoginForm()