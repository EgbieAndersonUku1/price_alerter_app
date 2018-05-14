from login.models.login import Login
from mall.models.mall import Mall
from password.models.password import Password
from registration.models.registration import Registration
from users.models.user_db import UserDB


class Account(object):
    """The user Account class"""

    def __init__(self, username, email):
        self.Login = Login()
        self.Register = Registration()
        self.Password = Password(username, email)
        self.Retrieve = _Account()
        self.Mall = Mall(username)


class _Account(object):
    """The methods relating to the user account"""

    def find_account_by_username(self, username):
        """Search for the user's account using their username"""
        return UserDB.objects.filter(username=username).first()

    def find_account_by_email(self, email):
        """Search for the user's account using their email address"""
        return UserDB.objects.filter(email=email).first()

    def get_account_status(self, email):
        """Returns the user account status"""

        account_status = None
        user = UserDB.objects.filter(email=email).only('email_confirmed').first()

        if not user:
            account_status = 'ACCOUNT_NOT_FOUND'
        elif not user.email_confirmed:
            account_status = 'EMAIL_NOT_CONFIRMED'
        elif user.email_confirmed:
            return 'ACCOUNT_CONFIRMED'
        return account_status

