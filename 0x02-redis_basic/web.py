#!/usr/bin/env python3
""" Model for the get_page function """
import redis
from requests import get
from functools import wraps
from typing import Callable


def cache_content(fn: Callable) -> Callable:
    """fuction to cache the content of respons"""
    @wraps(fn)
    def wrapper(url: str) -> str:
        """wraper to check if the content exist or not"""
        r = redis.Redis()
        content = r.get(url)
        name = f"count:{url}"
        r.incr(name)
        if content:
            return content.decode('utf-8')
        content = fn(url)
        r.setex(url, 10, content)
        r.set(f'count:{url}', 0)
        return content
    return wrapper


@cache_content
def get_page(url: str) -> str:
    """obtain the HTML content of a particular URL and returns it."""
    return get(url).text
