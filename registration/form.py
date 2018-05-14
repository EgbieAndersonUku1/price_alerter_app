from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.validators import ValidationError
from wtforms.fields.html5 import EmailField

from users import user


class RegisterForm(Form):
    """The Registration Form needed for the user to to register.
       This form will be displayed to user in the GUI
    """

    username = StringField('Username', validators=[validators.DataRequired(),
                                                   validators.Length(min=3, max=80),
                                                   ]
                           )
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.Length(min=3, max=80),
                                                     validators.EqualTo('confirm')
                                                     ]
                             )
    confirm = PasswordField('Confirm password')
    email = EmailField('Email address', validators=[validators.DataRequired()])

    def validate_email(form, field):
        """Checks if there is not already a user by that email address"""

        if user.Account.Retrieve.find_account_by_email(form.email.data):
            raise ValidationError('The email address already exists')

    def validate_username(form, field):
        """Checks if there is not already a user by that username"""

        if user.Account.Retrieve.find_account_by_username(form.username.data):
            raise ValidationError('The username already exists')