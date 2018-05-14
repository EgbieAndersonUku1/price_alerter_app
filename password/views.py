from flask import Blueprint, redirect, url_for, abort, render_template

from users.models.user import User
from password.forms import ForgottenPasswordForm, NewPasswordForm, ChangePasswordForm
from utils.decorators import login_required
from utils.security.sessions import Session

password_app = Blueprint('password_app', __name__, url_prefix='/password')


@password_app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    """This view function allows the user to request for a password reset link"""

    form, msg = ForgottenPasswordForm(), ''

    if form.validate_on_submit():
        user = User(email=form.email.data)

        if user.Account.Password.generate_forgotten_password_code():
            user.Account.Password.email_user_forgotten_password_code_link()
            return redirect(url_for('password_app.reset_link_sent'))

    return render_template('password/forgot_password.html', form=form)


@password_app.route('/reset/<username>/<code>', methods=['GET', 'POST'])
def password_reset(username, code):
    """password_reset(str, str) -> returns template

       The view function allows the user to reset their forgotten password

       :params
          `username`: The user's username
          `code`: The forgotten code sent to the user email account

       :returns
          returns a template
    """

    form, error = NewPasswordForm(), None
    user = User(username=username)

    if not user.Account.Password.is_forgotten_password_code_valid(code):
        abort(404)
    if form.validate_on_submit() and user.Account.Password.reset_password(form):
        user.Account.Password.email_user_about_password_change()
        return redirect(url_for('password_app.password_successful_changed'))

    return render_template('password/password_reset.html', form=form, error=error, username=username, code=code)


@password_app.route('/change', methods=['GET', 'POST'])
@login_required
def change_password():
    """The view function allows the user to change their current password"""

    form, error = ChangePasswordForm(), None
    user = User(email=Session.lookup('email'))

    if form.validate_on_submit():

        if user.Account.Password.change_old_password(form):

            user.Account.Password.email_user_about_password_change()
            Session.delete_login_credentials()
            return redirect(url_for('password_app.password_successful_changed'))

    return render_template('password/new_password.html', form=form)


@password_app.route('/msg/reset')
def reset_link_sent():
    """Returns a static template informing the user about password reset link"""
    return render_template('password/password_reset_msg.html')


@password_app.route('/changed_successful')
def password_successful_changed():
    """Returns a static template informing the user about the password change"""
    return render_template('password/password_changed.html')