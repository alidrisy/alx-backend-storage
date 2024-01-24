#!/usr/bin/env python3
""" Model for the class Cache """
import redis
import uuid
from typing import Union


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
