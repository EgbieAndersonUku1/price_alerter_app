from flask import session


class Session(object):

    @staticmethod
    def add(key, value):
        session[key] = value

    @staticmethod
    def delete(key):
        session.pop(key) if session.get('key') else None

    @staticmethod
    def lookup(key):
        return session.get(key)

    @staticmethod
    def delete_login_credentials():
        """"""
        if session.get('email'):
            session.pop('email')
        if session.get('login_token'):
            session.pop('login_token')

