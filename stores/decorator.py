from functools import wraps

from utils.cache.cache import Cache


def get_from_cache(f):
    """Using a key checks if the value for the key is already in the cache.
       If the value for the key is found returns the value associated with
       the key from the cache.

       If key is not found in the cache creates a new value for the key in
       the cache and returns the value for the key.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):

        key = args[1]  # args[1] -> store_name


        if len(key) != 32:
            return Cache.find_in_cache(key=key, value=f(*args, **kwargs).store_id)
        return Cache.find_in_cache(key=key, value=f(*args, **kwargs))

    return decorated_function


