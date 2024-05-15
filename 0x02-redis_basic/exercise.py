#!/usr/bin/env python3
'''A module for using the Redis NoSQL data storage.
'''
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union, Optional


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.

    Args:
        method (Callable): The method to track the number of calls.

    Returns:
        Callable: The wrapped method.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.

        Args:
            self: The instance of the class.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            Any: The result of the method call.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        # Create keys for input and output storage
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)

        # Store input in Redis
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))

        # Call the method and store its output
        output = method(self, *args, **kwargs)

        # Store output in Redis
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)

        return output
    return invoker


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
    @call_history
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


def replay(method: Callable):
    redis_instance = redis.Redis()
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    call_count = len(inputs)

    print(f"{method.__qualname__} was called {call_count} times:")

    for inp, out in zip(inputs, outputs):
        inp_str = inp.decode('utf-8')
        out_str = out.decode('utf-8')
        print(f"{method.__qualname__}(*{inp_str}) -> {out_str}")


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
