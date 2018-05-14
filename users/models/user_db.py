from mongoengine import signals

from app import db


class UserDB(db.Document):
    """Allows the user to save their details to the database"""

    username = db.StringField(db_field='u', required=True, unique=True)
    password = db.StringField(db_field='p', required=True, unique=True)
    email = db.EmailField(db_field='e', required=True, unique=True)
    email_confirmed = db.BooleanField(db_field='ec', default=False)
    configurations_codes = db.DictField(db_field='cc')

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """This function is called before the user values is saved to the database"""

        document.username = document.username.lower()
        document.email = document.email.lower()

    meta = {
        'indexes': ['username', 'email']
    }


signals.pre_save.connect(UserDB.pre_save, sender=UserDB)
