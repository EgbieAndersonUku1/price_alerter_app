from mongoengine.queryset.visitor import Q

from stores.decorator import get_from_cache
from stores.models.store_db import StoresDB
from mall.database.mall_db import MallDB
from users.models.user_db import UserDB
from utils.generator.code_generator import CodeGenerator
from utils.parser.parser import Parser
from utils.security.sessions import Session


class Store(object):
    """The Store class allows the user to create a brand new store"""

    def __init__(self, store_name, url_prefix, tag_name, query, description=None, store_id=None):
        self.store_id = store_id if store_id else CodeGenerator.generate_hex()
        self.store_name = store_name
        self.description = description
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query

    @classmethod
    @get_from_cache
    def get_store_id_by_name(cls, store_name):
        """"""
        return StoresDB.objects.filter(store_name=store_name).only('store_id').first()

    @classmethod
    @get_from_cache
    def get_store_by_id(cls, store_id):
        """"""
        return StoresDB.objects.get(store_id=store_id)

    @classmethod
    def get_store_fields(cls, page=1):
        """"""
        return StoresDB.objects.filter(predefined_store=True).only('store_name', 'description',
                                                                   'url_prefix', 'query', 'tag_name',
                                                                   'store_id').paginate(int(page), per_page=4)
    @classmethod
    def does_item_belong_to_store(cls, store_id, item_url):
        """"""
        store = StoresDB.objects.filter(store_id=store_id).only('url_prefix').first()
        return Parser.parse_url_prefix_from_url(item_url) == store.url_prefix

    def save(self):
        """"""
        store = self._get_obj_to_save()
        store.save()

        # look at this one tomoorow
        username = Session.lookup('username')
        mail = MallDB.objects.filter(username=username).first()
        user = UserDB.objects.filter(username=username).first()

        store.mall = mail
        store.user = user
        store.user_email = Session.lookup('email')
        store.save()

    def _get_obj_to_save(self):
        """"""
        return StoresDB(store_id=self.store_id,
                        store_name=self.store_name,
                        url_prefix=Parser.parse_url_prefix_from_url(self.url_prefix),
                        tag_name=self.tag_name,
                        query=self.query,
                        description=self.description,
                        )

    @classmethod
    def get_all_stores(cls, page):
        """"""
        return StoresDB.objects.filter(Q(predefined_store=False) &
                                       Q(user_email=Session.lookup('email'))
                                       ).order_by('creation_date').paginate(int(page), per_page=6)

    @staticmethod
    def get_all_predefined_stores(page):
        """returns all stores"""
        return StoresDB.objects.filter(predefined_store=True).paginate(int(page), per_page=6)

    def __repr__(self):
        return '<Store "{}">'.format(self.store_name)

    @classmethod
    def delete_store(cls, store_id):
        StoresDB.objects.filter(store_id=store_id).delete()