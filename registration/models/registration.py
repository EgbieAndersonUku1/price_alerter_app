import registration.constants as registration_constants
from app import app
from users.models.user_db import UserDB
from utils.email_sender.mailgun import MailGun
from utils.generator.code_generator import CodeGenerator
from utils.security.security import PasswordImplementer
from utils.url import construct_url


class Registration(object):
    """The Registration class allows a user to register their details to the application"""

    @staticmethod
    def is_registration_code_valid(username, code):
        """is_registration_code_valid(str, str) -> returns (bool)

        Takes a username and a registration code and checks if the
        code attributed to the user is valid. Returns True if it
        is or False if it is not.

        :param
            `username`: The username the user has registered with.
            `code`: The code sent when the user registered their details
        :returns
            Returns True if the registration code is valid or False otherwise
        """

        user = UserDB.objects.filter(username=username).first()

        if user and user.configurations_codes.get('registration_code') == code:
            user.email_confirmed = True
            user.configurations_codes = {}
            user.save()
            return True
        return False

    @classmethod
    def register(cls, registration_form):
        """register(form object) -> returns None

        Takes the user's registration details and saves it to
        the database

        :param
           `registration_form` : The form object contains the user's registration
                                 details e.g username, email, etc.
        """

        code = CodeGenerator.generate_code()
        user = UserDB(username=registration_form.username.data,
                      email=registration_form.email.data,
                      password=PasswordImplementer.hash_password(registration_form.password.data),
                      configurations_codes={'registration_code': code},
                      )
        user.save()
        cls._email_registration_code(user)

    @classmethod
    def _email_registration_code(cls, user):
        """_email_registration_code(user obj) -> returns None

           A private that is called once the user's details has been entered.
           The method emails the user's their registration code
        """
        url = construct_url('confirm', user.username, user.configurations_codes.get('registration_code'))

        MailGun.send_email(user.email, registration_constants.SUBJECT,
                           registration_constants.BODY.format(user.username.title(), url)
                           )
