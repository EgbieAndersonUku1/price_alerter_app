from unittest import TestCase

from stores.models import Store
from app import create_app as create_app_base


class StoreTest(TestCase):

    def create_app(cls):

        DB_NAME = 'store_test'

        return create_app_base(
            MONGODB_DB={'DB': DB_NAME},
            TESTING=True,
            CSRF_ENABLED=False

        )

    def setUpClass(cls):
        cls.app = cls.create_app()
