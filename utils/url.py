from app import app


def construct_url(action, username, code):
    """Construct a url"""
    return '{}/{}/{}/{}'.format(get_url(), action, username, code)


def get_url():
    """Returns the host URL"""
    return app.config['HOSTNAME']