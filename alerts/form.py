from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import FloatField


class BaseAlertForm(FlaskForm):
    """The base alert form that enables the user to enter an alert"""

    alert_limit = FloatField('Alert price',
                             validators=[validators.DataRequired(
                                 message='This field must be an integer or a float')
                             ]
                             )


class NewAlertForm(BaseAlertForm):
    pass


class EditAlertForm(BaseAlertForm):
    pass


