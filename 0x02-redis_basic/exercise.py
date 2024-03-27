#!/usr/bin/env python3
'''Learning redis with python'''

import uuid
import redis
from functools import wraps
from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    '''Decorator to count the number of calls'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function'''
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    '''Decorator to store the history of inputs and outputs'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''Wrapper function'''
        self._redis.rpush(f"{key}:inputs", str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(f"{key}:outputs", str(data))
        return data
    return wrapper


class Cache:
    '''Cache class'''
    def __init__(self):
        '''Constructor'''
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Store data in redis'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Get data from redis'''
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        '''Get string data from redis'''
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        '''Get int data from redis'''
        return self.get(key, int)
