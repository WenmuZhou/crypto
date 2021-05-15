#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/30 16:03
# @Author   : Adolf
# @File     : class_ray.py
# @Function  :
import ray
import random

ray.init()


@ray.remote
class Counter(object):
    def __init__(self, n):
        self.n = n

    def increment(self):
        self.n += 2

    def read(self, a):
        return self.n + a


# counters = [Counter.remote(n=i) for i in range(6)]
counters = [Counter.remote(n=1)]
[c.increment.remote() for c in counters]
futures = [c.read.remote(a=3) for c in counters]
print(ray.get(futures))
