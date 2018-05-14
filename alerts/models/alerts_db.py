from mongoengine import signals, CASCADE

from app import db
from items.model.item_db import ItemDB
from utils.time_now import time_now


class AlertsDB(db.Document):
    """The database model for the Alerts."""

    alert_id = db.StringField(db_field='ai', required=True)
    price_limit = db.FloatField(db_field='pl', required=True)
    last_checked = db.DateTimeField(db_field='lc', default=time_now())
    email = db.EmailField(db_field='e', required=True)
    active = db.BooleanField(db_field='a', default=True)
    item = db.ReferenceField(ItemDB, reverse_delete_rule=CASCADE)
    creation_date = db.DateTimeField(db_field='cd', default=time_now())

    meta = {
        'indexes': ['alert_id', 'active', 'email',
                    'last_checked', 'price_limit', 'creation_date']
    }


