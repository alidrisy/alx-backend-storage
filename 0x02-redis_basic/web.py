#!/usr/bin/env python3
""" Model for the get_page function """
import redis
from requests import get


def get_page(url: str) -> str:
    """obtain the HTML content of a particular URL and returns it."""
    r = redis.Redis()
    content = get(url)
    name = f"count:{url}"
    r.incr(name)
    r.expire(name, 10)
    return content.text
