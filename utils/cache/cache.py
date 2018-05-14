from app import cache


class Cache(object):
    """The class allows the user to save data to the cache. The class
       also allows the user to access the cache as well as deleting the
       cache
    """

    @classmethod
    def find_in_cache(cls, key, func=None, value=None, fetch_new=False):
        """find_in_cache(str, func, value, boolean) -> returns None or cached value

           Takes a key and uses it to access the cache for the value relating to that key. If the
           key is found in the cache returns the value associated with that key.
           If the key is not found within the cache executes a function and stores the value for
           that function as the value for that key and returns the executed function value

           :parameter
                `key`: This is a unique key associated with a value in the cache
                `func`: The function when executed returns a value and stores that value along with the
                        key in the cache
                `value`: A value that can be stored along with the key in the cache
                `fetch_new`: When the value is set to true does not returned a cached valued but
                             instead returns a new value
        """
        if fetch_new:
            return cls._get_new(key, func)

        rv = cache.get(key)

        if rv:
            return rv
        elif rv is None and func:
            value = func()
        if value is not None:
            cls.save_to_cache(key=key, value=value)
        return value

    @classmethod
    def delete_from_cache(cls, key):
        """delete_from_cache(str) -> returns None

           `key`: Takes a key and deletes the value associated with that key
                  from the cache
        """
        cache.delete(key)

    @classmethod
    def _get_new(cls, key, func):
        """_get_new(str, func) -> returns (str)

           Executes, saves and returns a new value associated with the key instead of a cached value

           `key`: A new key for the item
           `func`: A func that when executes returns a new value
        """
        return cls.save_to_cache(key=key, value=func())

    @classmethod
    def save_to_cache(cls, key, value):
        """"""
        cache.set(key, value, timeout=100)
        return value
