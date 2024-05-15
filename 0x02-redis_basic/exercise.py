#!/usr/bin/env python3
'''A module for using the Redis NoSQL data storage.
'''
import uuid
import redis
import functools
from typing import Any, Callable, Union, Optional


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args:
        method: The method to be decorated.

    Returns:
        The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper for the decorated method.

        Args:
            self: The instance of the class.
            *args: The positional arguments passed to the method.
            **kwargs: The keyword arguments passed to the method.

        Returns:
            The result of the original method.
        """
        # Increment the call count
        self._redis.incr(method.__qualname__)
        # Call the original method
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    A class for storing and retrieving data from Redis using UUIDs as keys.

    Attributes:
        self._redis (redis.Redis): A Redis client instance.

    Methods:
        __init__(): Initialize a Redis client instance and clear the database.
        store(data): Store the data in Redis with a UUID key and
        return the key.
    """

    def __init__(self):
        """
        Initialize a Redis client instance and clear the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis with a UUID key and return the key.

        Args:
            data: The data to be stored. Can be a string, bytes, int, or float.

        Returns:
            str: The UUID key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Optional[Callable[[Any], Union[str, bytes, int, float]]] = None
            ) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieves a value from a Redis data storage.

        Args:
            key: The key of the data to be retrieved.
            fn: An optional function to apply to the retrieved data.

        Returns:
            The retrieved data, optionally transformed by the function.
        """
        # Retrieve the data from Redis
        data = self._redis.get(key)

        # Apply the function to the data (if provided)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves a string value from a Redis data storage.

        Args:
            key: The key of the data to be retrieved.

        Returns:
            The retrieved string value.
        """
        # Retrieve the data using the get method
        data = self.get(key)

        # Check if data is None
        if data is None:
            return None

        # Convert data to string and return
        return str(data)


def get_int(self, key: str) -> Optional[int]:
    """
    Retrieves an integer value from a Redis data storage.

    Args:
        key: The key of the data to be retrieved.

    Returns:
        The retrieved integer value.
    """

    # Retrieve the data using the get method
    data = self.get(key)

    # Check if data is None
    if data is None:
        return None

    # Convert data to an integer and return
    return int(data)


# # Example usage:
# if __name__ == "__main__":
#     cache = Cache()

#     TEST_CASES = {
#         b"foo": None,
#         123: int,
#         "bar": lambda d: d.decode("utf-8")
#     }

#     for value, fn in TEST_CASES.items():
#         key = cache.store(value)
#         assert cache.get(key, fn=fn) == value
