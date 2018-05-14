from uuid import uuid4


class _Generator(object):
    """"""
    def generate_code(self):
        raise NotImplementedError

    def generate_hex(self):
        raise NotImplementedError


class CodeGenerator(_Generator):
    """"""

    @staticmethod
    def generate_code():
        """Returns a 32 bit character string"""
        return str(uuid4())

    @staticmethod
    def generate_hex():
        """Returns a 32 bit hex decimal string"""
        return uuid4().hex