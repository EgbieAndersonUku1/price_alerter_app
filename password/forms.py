from flask_wtf import FlaskForm
from wtforms import validators, PasswordField
from wtforms.fields.html5 import EmailField


class BasePasswordForm(FlaskForm):
    """"""
    password = PasswordField('New password', validators=[validators.DataRequired(),
                                                         validators.Length(min=3, max=80),
                                                         validators.EqualTo('confirm')
                                                         ]
                             )
    confirm = PasswordField('Repeat password')


class NewPasswordForm(BasePasswordForm):
    pass


class ForgottenPasswordForm(FlaskForm):
    """"""
    email = EmailField('Email', validators=[validators.DataRequired()])


class ChangePasswordForm(BasePasswordForm):
    """"""
    current_password = PasswordField('Current password', validators=[validators.DataRequired(),
                                                                     validators.Length(min=3, max=80),
                                                                     ]
                                     )

