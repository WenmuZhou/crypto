#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/8 20:15
# @Author  : Adolf
# @File    : test.py
import ray

ray.init()


@ray.remote
def f(x):
    return [x, x * x, x * x * x]


futures = [f.remote(i) for i in range(4)]
print(ray.get(futures))
