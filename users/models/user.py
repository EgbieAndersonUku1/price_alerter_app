from users.models.account import Account


class User(object):
    """The user class object allows the user to access all things relating to their account"""
    def __init__(self, username=None, email=None, mall_id=None):
        self.Account = Account(username=username, email=email)









