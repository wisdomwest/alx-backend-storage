#!/usr/bin/env python3
''' Implementing an expiring web cache and tracker'''

import requests
import redis
from functools import wraps
from typing import Callable


r = redis.Redis()


def count_requests(method: Callable) -> Callable:
    '''track how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds'''
    @wraps(method)
    def wrapper(url) -> str:
        '''wrapper function'''
        r.incr(f'count:{url}')
        cached = r.get(f'cached:{url}')
        if cached:
            return cached.decode('utf-8')
        cached = method(url)
        r.set(f'count:{url}', 0)
        r.setex(f'cached:{url}', 10, cached)
        return cached
    return wrapper


@count_requests
def get_page(url: str) -> str:
    '''Gets the HTML content of a particular URL and returns it'''
    return requests.get(url).text
