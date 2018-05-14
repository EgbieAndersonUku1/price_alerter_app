from flask import Blueprint, render_template, request, abort, url_for, redirect

from registration.form import RegisterForm
from users import user
from utils.messenger.flash_messenger import Message
from utils.decorators import is_user_already_logged_in as is_user_already_registered
from utils.security.sessions import Session

registration_app = Blueprint('registration_app', __name__)


@registration_app.route('/register', methods=['GET', 'POST'])
@registration_app.route('/register/', methods=['GET', 'POST'])
@is_user_already_registered
def register():
    """Register the user's details to the application"""

    form = RegisterForm()

    if form.validate_on_submit() and request.method == 'POST':

        user.Account.Register.register(registration_form=form)
        Message.display_to_gui_screen('You need to verify your account to use price alerter')

    return render_template("registration/register.html", form=form)


@registration_app.route('/confirm/<username>/<code>')
def confirm(username, code):
    """confirm(str, str) -> returns 404 not found page or redirect to login page

       Checks if the user's username and registration code is valid. Returns
       a 404 not found page if username and code is invalid, otherwise
       redirects the user to the login screen.
    """

    if not user.Account.Register.is_registration_code_valid(username, code):
        abort(404)

    Session.add('username', username)
    user.Account.Mall.username = username
    user.Account.Mall.save_generated_mall_id()
    return redirect(url_for('login_app.login'))