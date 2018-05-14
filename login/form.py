from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms import validators, PasswordField


class LoginForm(FlaskForm):
    """The Login Form allows the user to login from the GUI"""

    email = EmailField('Email', validators=[validators.DataRequired(),
                                                   validators.Length(min=3, max=80),
                                                   ]
                           )
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.Length(min=3, max=80)
                                                     ]
                             )