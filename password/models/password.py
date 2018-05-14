from users.models.user_db import UserDB
from utils.email_sender.mailgun import MailGun
from utils.generator.code_generator import CodeGenerator
from utils.security.security import PasswordImplementer
from utils.security.sessions import Session
from password.constants_templates import reset_password as reset_password_constant
from password.constants_templates import password_changed as password_changed_constant
from utils.url import construct_url


class Password(object):
    """"""

    def __init__(self, username, email):

        if username:
            self._user = UserDB.objects.filter(username=username).first()
        elif email:
            self._user = UserDB.objects.filter(email=email).first()

    def change_old_password(self, password_form):
        """"""
        self._user.password = PasswordImplementer.hash_password(password_form.password.data)
        self._user.save()
        return True

    def generate_forgotten_password_code(self):
        """"""
        if self._user:

            self._user.configurations_codes['forgotten_password_code'] = CodeGenerator.generate_code()
            self._user.save()

            return True
        return None

    def email_user_forgotten_password_code_link(self):
        """Emails the user the reset password link.
           This method assumes that the generate_forgotten_password_code
           was called first.
        """
        url = construct_url('password/reset', self._user.username, self._user.configurations_codes.get('forgotten_password_code'))
        MailGun.send_email(self._user.email, reset_password_constant.SUBJECT,
                           reset_password_constant.BODY.format(self._user.username.title(), url)
                           )

    def is_forgotten_password_code_valid(self, code):
        """"""
        return self._user.configurations_codes.get('forgotten_password_code') == code if self._user else False

    def reset_password(self, password_form):
        """reset_password(form-object) -> returns bool

           Allows the user to reset their password. This method assumes that the
           forgotten password code was called first.
        """

        self._user.password = PasswordImplementer.hash_password(password_form.password.data)
        self._user.save()
        Session.delete('login_token')

        return True

    def email_user_about_password_change(self):
        """Informs the user that their password has been changed. The
           method assumes that the user is a valid user.
        """
        MailGun.send_email(self._user.email, password_changed_constant.SUBJECT,
                           password_changed_constant.BODY % (self._user.username.title()))


