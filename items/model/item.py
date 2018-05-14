from os.path import join
from mongoengine.queryset.visitor import Q
from mongoengine.errors import NotUniqueError

from items.model.item_db import ItemDB
from settings import STATIC_IMAGE_URL
from stores.models.store import Store
from utils.cache.cache import Cache
from utils.generator.code_generator import CodeGenerator
from utils.parser.parser import Parser
from utils.security.sessions import Session


class Item(object):
    """The Item class allows the user to create any item within a store.
       The item class assumes that the store is already created and therefore
       must not be called on its own.

       Any item created belongs to store it's created under and as such
       if the store that represents the item is ever deleted the items that were
       created are also deleted.
    """

    def __init__(self, store_id, item_name='', url='',  description='', item_id=None, item_image=None, _id=None):
        self.item_id = item_id if item_id else CodeGenerator.generate_hex()
        self.item_name = item_name
        self.url = url
        self.item_image = item_image
        self.description = description
        self.price = None
        self.alert_id = None
        self.alert_added = False
        self.alert_deleted = False
        self.store_id = store_id
        self.store = Store.get_store_by_id(store_id)
        self._id = _id

    def load_price(self, fetch_new=False):
        """load_price(boolean) -> returns flask pagination object

           The load_price method allows the user to load a price for a
           given item from the cache. Since the price is loaded from the
           cache it is not always the currently price. To get the latest price
           run the method with the `fetch_new` parameter set to True.

        """
        self.price = Cache.find_in_cache(key=self.item_id, func=self._fetch_price, fetch_new=fetch_new)

    def _fetch_price(self):
        """The fetch_price method fetches a new price from the item's website"""
        return Parser.parse_price_from_url_page(self.url, self.store.tag_name, self.store.query)

    @staticmethod
    def modify_field(item_id, values):
        """modify_field(str, dict) -> returns boolean

           Allows the user to modify an existing row's or collections in the database
           with a new value.

           `item_id`: The item in the database. This will be modified by the user.
           `values` : The updated value

        """
        assert type(values) == dict
        return ItemDB.objects.filter(item_id=item_id).modify(**values, new=True)

    def save(self):
        """Saves the entire item to the database"""
        item = self._get_obj_to_save()

        try:
            item.save()
        except NotUniqueError:
            return False

        item.store = self.store
        item.save()

        return True

    def _get_obj_to_save(self):
        """Retrieves the object that will be saved to the database"""

        item = ItemDB(item_name=self.item_name,
                      url=self.url,
                      item_id=self.item_id,
                      user_email=Session.lookup('email'),
                      store_id=self.store_id,
                      item_description=self.description,
                      )
        if self.item_image:
            item.item_image = self._get_image_path()
        return item

    def _get_image_path(self):
        """Returns the item's image path"""
        return join(STATIC_IMAGE_URL, 'user', self.item_image)

    @staticmethod
    def get_items_with_no_alerts(page=1):
        """"""
        return ItemDB.objects(Q(alert_added=False) &
                              Q(user_email=Session.lookup('email'))
                              ).paginate(page, per_page=9)

    @classmethod
    def get_item(cls, item_id):
        """Returns the Item class and not Item documents DB using the item's ID
           or returns None if not found
        """

        item = cls.get_item_by_id(item_id)

        if item:
            item_obj = cls(item_name=item.item_name,
                           url=item.url,
                           store_id=item.store.store_id,
                           item_id=item.item_id,
                           item_image=item.item_image,
                           description=item.item_description,
                           _id=item.id,
                           )
            item_obj.alert_deleted = item.alert_deleted
            item_obj.alert_added = item.alert_added
            item_obj.alert_id = item.alert_id

            return item_obj

    @staticmethod
    def get_items_by_store_id(store_id, page):
        """get_items_by_store_id(str, int) -> returns Flask pagination object

           Takes a store ID and returns all items belong to that particular store

           :parameter
                `store_id`: The store id containing the entire store items
                 `page`:    The GUI page containing the items
        """
        return ItemDB.objects.filter(store_id=store_id).order_by('-creation_date').paginate(int(page), per_page=9)

    @classmethod
    def get_item_by_id(cls, item_id):
        """get_item_by_id(str) -> returns Item document object or None

           :param
              `item_id`: A hex-decimal string that represents the item within the database

           Query the database using item's ID returns the item's database object if found
           else None
        """
        return ItemDB.objects.filter(item_id=item_id).first()

    def __repr__(self):
        return '<Item "{}">'.format(self.item_name)

    @classmethod
    def delete_item(cls, item_id):
        """delete_item(str) -> returns None

           Takes a string in the form of an item ID and uses that to delete
           the item from the database
        """
        ItemDB.objects.filter(item_id=item_id).delete()
