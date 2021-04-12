#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/12 14:23
# @Author   : Adolf
# @File     : scikit_lib.py
# @Function  :
import numpy as np
from sko.GA import GA


# def schaffer(p):
#     '''
#     This function has plenty of local minimum, with strong shocks
#     global minimum at (0,0) with value 0
#     '''
#     x1, x2 = p
#     x = np.square(x1) + np.square(x2)
#     return 0.5 + (np.square(np.sin(x)) - 0.5) / np.square(1 + 0.001 * x)
#
#
# ga = GA(func=schaffer, n_dim=2, size_pop=50, max_iter=800, lb=[-1, -1], ub=[1, 1], precision=1e-7)
# best_x, best_y = ga.run()
# print('best_x:', best_x, '\n', 'best_y:', best_y)

def task(p):
    x1, x2, x3, x4 = p
    return -(x1 ** 2 + x2 ** 2 + x3 ** 3 + x4 ** 4)


ga = GA(func=task, n_dim=4, size_pop=100, max_iter=1000, lb=[1, 1, 1, 1], ub=[30, 30, 30, 30], prob_mut=0.1, precision=1)
best_x, best_y = ga.run()
print('best_x:', best_x, '\n', 'best_y:', best_y)
