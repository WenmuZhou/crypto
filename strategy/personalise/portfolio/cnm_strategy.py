#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/7 15:21
# @Author   : Adolf
# @File     : cnm_strategy.py
# @Function  :
import os
import pandas as pd

pd.set_option("expand_frame_repr", False)

stock_dir = "dataset/stock/stock_handle/"
stock_pool = os.listdir(stock_dir)
# print(stock_pool)

for stock in stock_pool:
    # print(stock)
    if stock != "600570.csv":
        continue
    stock_path = os.path.join(stock_dir, stock)
    stock_df = pd.read_csv(stock_path)
    print(stock_df)
