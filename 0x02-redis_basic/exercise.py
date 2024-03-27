#!/usr/bin/env python3
'''Learning redis with python'''

import uuid
import redis
from typing import Union, Callable


class Cache:
    '''Cache class'''
    def __init__(self):
        '''Constructor'''
        self._redis = redis.Redis()
        self._redis.flushdb()

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
