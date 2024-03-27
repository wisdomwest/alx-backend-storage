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


def replay(fn: Callable) -> None:
    '''implement a replay function to display the history
    of calls of a particular function'''
    name = fn.__qualname__

    input = f"{name}:inputs"
    output = f"{name}:outputs"
    count = 0

    print(f"{name} was called {count} times:")

    fn_inputs = self._redis.lrange(input, 0, -1)
    fn_outputs = self._redis.lrange(output, 0, -1)

    for i, o in zip(fn_inputs, fn_outputs):
        count += 1
        print(f"{name}(*{i.decode('utf-8')}) -> {o.decode()}")


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
