# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/6/13 21:17
# @Author  : Adolf
# @File    : cnm_strategy.py
# @Function:
import pandas as pd

pd.set_option("expand_frame_repr", False)

df = pd.read_csv("dataset/stock/stock_used.csv")
print(df)