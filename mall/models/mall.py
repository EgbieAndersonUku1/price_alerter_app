from mongoengine import signals

from mall.database.mall_db import MallDB
from utils.generator.code_generator import CodeGenerator


class Mall(object):
    """"""
    def __init__(self, username):
        self.mall_id = CodeGenerator.generate_hex()
        self.username = username

    def save_generated_mall_id(self):
        MallDB(mall_id=self.mall_id, username=self.username).save()
