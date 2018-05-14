from mongoengine import signals, CASCADE

from stores.models.store_db import StoresDB
from app import db
from utils.time_now import time_now


class ItemDB(db.Document):
    """The fields for the item that would be saved to the database"""
    item_id = db.StringField(required=True)
    store_id = db.StringField(db_field='si', required=True, default='')
    alert_id = db.StringField(db_field='ai')
    url = db.URLField(db_field='u', required=True, unique=True)
    item_name = db.StringField(db_field='in', required=True)
    item_image = db.StringField(db_field='i')
    item_description = db.StringField(db_field='d')
    user_email = db.StringField(db_field='ue', required=True)
    alert_added = db.BooleanField(db_field='aa', default=False)
    store = db.ReferenceField(StoresDB, reverse_delete_rule=CASCADE)
    creation_date = db.DateTimeField(db_field='cd', default=time_now())
    alert_deleted = db.BooleanField(db_field='ad', default=False)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """A pre-save function that is called before any item is saved"""
        document.item_name = document.item_name.lower()
        document.url = document.url.lower()

    meta = {
        'indexes': ['url', 'user_email', 'alert_added', 'store', 'item_id']
    }


signals.pre_save.connect(ItemDB.pre_save, sender=ItemDB)

