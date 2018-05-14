from flask_wtf import FlaskForm
from validators import url as url_validator

from wtforms import validators, StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import ValidationError
from flask_wtf.file import FileField, FileAllowed

from items.model.item_db import ItemDB
import items.constant as item_constant



class BaseItemForm(FlaskForm):
    """The base item form for the items"""
    description = StringField('Description', validators=[validators.Length(min=69, max=255)])


class ItemForm(BaseItemForm):
    """Represents the fields that will be displayed to the user in GUI fields"""

    url = URLField('Item URL', validators=[validators.Required()])
    item_name = StringField('Item name', validators=[validators.DataRequired(),
                                                     validators.Length(max=60),
                                                     ]
                            )

    image = FileField('Item image (optional)', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                                                                       'Only JPEG, PNG and GIFs allowed')
                                                           ])
    def validate_url(form, field):
        """validate_url(form obj, field obj) -> returns None

           Validates the URl in three ways:

           1) First check whether the URL entered by the user is correct
           2) Second, validates whether the URL's prefix for the item belongs
              to the store the item is been created under.
           3) Third, checks whether the item's URL already exists
        """
        if not url_validator(form.url.data):
            raise ValidationError('The url entered has an incorrect form')
        if ItemDB.objects.filter(url=form.url.data).first():
            raise ValidationError(item_constant.DUPLICATE_ITEM)
