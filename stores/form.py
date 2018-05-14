from flask_wtf import FlaskForm
from wtforms.fields.html5 import URLField
from wtforms import validators, StringField


class BaseStoreForm(FlaskForm):

    store_name = StringField('Store name', validators=[validators.DataRequired(),
                                                       validators.Length(max=30)
                                                       ])
    url_prefix = URLField('Store Url prefix', validators=[validators.DataRequired()])
    description = StringField('Description', validators=[validators.Length(max=255)])
    tag_name = StringField('Tag name', validators=[validators.DataRequired()], default='span')
    query = StringField('Store search query', validators=[validators.DataRequired()], default='{"id": "price-now"}')


class NewStoreForm(BaseStoreForm):
    pass


class EditStoreForm(FlaskForm):
    description = StringField('Description', validators=[validators.Length(max=255)])








