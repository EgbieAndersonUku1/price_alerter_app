from mongoengine import signals

from app import db


class MallDB(db.Document):
    """"""
    mall_id = db.StringField(db_field='mi', required=True)
    username = db.StringField(db_field='u', unique=True, required=False)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """"""
        document.username = document.username.lower()

    meta = {
        'indexes': ['username']
    }


signals.pre_save.connect(MallDB.pre_save, sender=MallDB)
