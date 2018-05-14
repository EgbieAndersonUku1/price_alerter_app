from users.models.user_db import UserDB

from utils.generator.code_generator import CodeGenerator as LoginToken
from utils.security.security import PasswordImplementer
from utils.security.sessions import Session


class Login(object):
    """Allows the user to login into the application"""

    @staticmethod
    def set_login_sessions(email):
        """Set the user's email to the secure session"""
        Session.add('email', email)

    @classmethod
    def login(cls):
        """Logs the user into the application. This method assumes that
           the user's login credentials is correct because it has be validated
           by the is_login_valid method.
        """
        if not Session.lookup('email'):
            raise Exception('<set_login_sessions> must be called before the login method')
        Session.add('login_token', LoginToken.generate_code())

    @classmethod
    def is_login_valid(cls, email, password):
        """is_login_valid(str, str) -> returns Bool or string

           Checks if the user's login credential is valid.
           Returns True if it is, False if password invalid
           or the account does not exists.

           :params
               `email`: The email address needed for the login process
               `password`: The user's password

        """
        user = UserDB.objects.filter(email=email).first()

        if user:
            return PasswordImplementer.check_password(password, hash_password=user.password)
        return False