from mongoengine import signals, CASCADE

from app import db
from mall.database.mall_db import MallDB
from users.models.user_db import UserDB
from utils.time_now import time_now


class StoresDB(db.Document):
    """"""

    store_id = db.StringField(required=True)
    store_name = db.StringField(db_field='sn', max_length=30, required=True, unique=True)
    description = db.StringField(db_field='d', max_length=900, required=True)
    url_prefix = db.URLField(db_field='up', required=True, unique=True)
    tag_name = db.StringField(db_field='tn', required=True)
    query = db.DictField(db_field='q', required=True)
    predefined_store = db.BooleanField(db_field='ps', default=False)
    mall = db.ReferenceField(MallDB, reverse_delete_rule=CASCADE)
    user = db.ReferenceField(UserDB, reverse_delete_rule=CASCADE)
    user_email = db.EmailField(db_field='ue')
    creation_date = db.DateTimeField(db_field='cd', default=time_now())

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """"""

        document.store_name = document.store_name.title()
        document.url_prefix = document.url_prefix.lower()
        document.tag_name = document.tag_name.lower()

    meta = {
        'indexes': ['store_name', 'url_prefix', 'store_id', 'predefined_store']
    }


signals.pre_save.connect(StoresDB.pre_save, sender=StoresDB)
