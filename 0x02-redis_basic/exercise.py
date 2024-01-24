#!/usr/bin/env python3
""" Model for the class Cache """
import redis
import uuid
from typing import Union, Callable, Any, Optional


class Cache:
    """ Class to Caching data using Redis """
    def __init__(self):
        """Initialize data"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
