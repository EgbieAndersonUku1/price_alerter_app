from mongoengine.queryset.visitor import Q

from alerts.models.alerts_db import AlertsDB
from items.model.item import Item
from utils.email_sender.mailgun import MailGun
from utils.generator.code_generator import CodeGenerator
from utils.security.sessions import Session
from utils.time_now import time_now
from utils.time_now import time_passed_since_current_time


class Alert(object):
    """The Alert class allows the user to set a price limit
       for any item. Once that price has been reached for the
       item the class then emails the user about the new price
    """

    def __init__(self, price_limit, item_id, active=True, last_checked=None, alert_id=None):
        self.price_limit = price_limit
        self.item_id = item_id
        self.item = None
        self.last_checked = last_checked
        self.email = Session.lookup('email')
        self.alert_id = alert_id if alert_id else CodeGenerator.generate_hex()
        self.active = active

    @staticmethod
    def get_alerts(page):
        """Returns all items that the user has placed an alert on"""
        return AlertsDB.objects.filter(email=Session.lookup('email'),
                                       active=True,
                                       ).paginate(page, per_page=9)

    @staticmethod
    def get_alert_by_id(alert_id):
        """Returns an alert by its ID"""

        return AlertsDB.objects.filter(alert_id=alert_id).first()

    @staticmethod
    def delete_alert_by_id(item_id, alert_id):
        """"""
        Item.modify_field(item_id, {'alert_added': False})
        Item.modify_field(item_id, {'alert_deleted': True})
        AlertsDB.objects(alert_id=alert_id).delete()

    @staticmethod
    def get_items_to_update(page, minutes=20):
        """Every twenty minutes the method returns a series items that will be
           updated with the new price
        """

        last_checked = time_passed_since_current_time(minutes=minutes)
        return AlertsDB.objects.filter(Q(user_email=Session.lookup('email')) &
                                       Q(last_checked__lte=last_checked)
                                       ).paginate(page, per_page=9)

    @classmethod
    def load_alert(cls, alert_id):
        """"""
        alert = cls.get_alert_by_id(alert_id)

        alert_obj = Alert(price_limit=alert.price_limit,
                          item_id=alert.item.item_id,
                          active=alert.active,
                          last_checked=alert.last_checked,
                          alert_id=alert.alert_id
                          )

        alert_obj.item = Item(item_name=alert.item.item_name,
                              url=alert.item.url,
                              store_id=alert.item.store.store_id,
                              item_id=alert.item.item_id
                              )  # load the item object into the alert obj
        return alert_obj

    def load_price(self, fetch_new=False):
        """Loads the items prices from database"""

        self.item.load_price(fetch_new)
        self.update({'last_checked': time_now()})
        return self.item.price

    def send_email_to_user_if_item_matches_price_limit(self):
        """Sends an email to the user once the item price has reached a certain limit"""

        self._send_alert() if self.item.price <= self.price_limit else None

    def save(self):
        """Saves the Alert's attributes to the database"""

        alert_db = AlertsDB(alert_id=self.alert_id,
                            price_limit=self.price_limit,
                            email=self.email,
                            last_checked=self.last_checked
                            )

        item = Item.get_item_by_id(self.item_id)
        item.alert_id = alert_db.alert_id

        if item.alert_deleted:
            item.alert_deleted = False

        item.save()
        alert_db.item = item

        return alert_db.save()

    def update(self, updates):
        """"""
        assert type(updates) == dict
        return AlertsDB.objects.filter(alert_id=self.alert_id).modify(**updates, new=True)

    @staticmethod
    def deactivate_alert(item_id, alert_id):
        """"""
        Item.modify_field(item_id, {'alert_added': False})
        AlertsDB.objects.filter(alert_id=alert_id).modify(**{'active': False})

    @staticmethod
    def activate_alert(item_id, alert_id):
        """"""
        Item.modify_field(item_id, {'alert_added': True})
        AlertsDB.objects.filter(alert_id=alert_id).modify(**{'active': True})

    def _send_alert(self):
        """A helper function that allows sends an email to the user informing them
           of the price change
        """
        subject = 'Price alert for item {}'.format(self.item.item_name)
        body = 'The item prices has now be lowered. Buy it now!!'

        MailGun.send_email(email=self.email, subject=subject, body=body)

    def __repr__(self):
        return "<Alert for User '' with item '{}' with price '{}'>".format(Session.lookup('username'),
                                                                           self.item.item_name,
                                                                           self.price_limit)
