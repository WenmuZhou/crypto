#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/11 10:33
# @Author   : Adolf
# @File     : matplotlib.py
# @Function  :
import numpy as np
import matplotlib.pyplot as plt

xs = np.linspace(-np.pi, np.pi, 30)
ys = np.sin(xs)
markers_on = [1, 2, 3, 4]
plt.plot(xs, ys, '-gD', markevery=markers_on)
plt.show()
