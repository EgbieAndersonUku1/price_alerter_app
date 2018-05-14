from passlib.hash import pbkdf2_sha512
from werkzeug import secure_filename
from urllib.parse import urlparse, urljoin
from flask import request, url_for


class PasswordImplementer(object):
    """"""

    @staticmethod
    def hash_password(password):
        """"""
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_password(password, hash_password):
        return pbkdf2_sha512.verify(password, hash_password)


def make_secure_file_name(file_name):
    """"""
    return secure_filename(file_name)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc