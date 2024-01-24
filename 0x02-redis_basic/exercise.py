#!/usr/bin/env python3
""" Model for the class Cache """
import redis
import uuid
from typing import Union, Callable, Any, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """increments the count for that key every time the method is called
    and returns the value returned by the original method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for increments the count"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """increments the count for that key every time the method is called
    and returns the value returned by the original method."""
    @wraps(method)
    def wrapper(self, *args):
        """wrapper for increments the count"""
        incr = method.__qualname__
        input_key = "{}:inputs".format(incr)
        output_key = "{}:outputs".format(incr)
        self._redis.rpush(input_key, str(args))
        output = method(self, *args)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


class Cache:
    """ Class to Caching data using Redis """
    def __init__(self):
        """Initialize data"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data:  Union[str, bytes, int, float]) -> str:
        """store data in Redis using the random key and return the key."""
        id: str = str(uuid.uuid4())
        self._redis.set(id, data)
        return id

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """covert the data that get using key from Redis by fn"""

        data = self._redis.get(key)
        if fn is str:
            return self.get_str(data)
        if fn is int:
            return self.get_int(data)
        if callable(fn):
            return fn(data)
        return data

    def get_str(self, data: bytes) -> str:
        """convert data from bytes to string"""
        return data.decode("utf-8")

    def get_int(self, data: bytes) -> int:
        """convert data from bytes to integer"""
        return int(data)
