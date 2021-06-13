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

min_len = 99999
code_id = ""
for stock in stock_pool:
    # print(stock)
    # if stock != "600570.csv":
    #     continue
    stock_path = os.path.join(stock_dir, stock)
    stock_df = pd.read_csv(stock_path)
    stock_df["code"] = stock.split(".csv")[0]

    if len(stock_df) < min_len:
        min_len = len(stock_df)
        code_id = stock
    # print(stock_df)

# print(min_len)
# print(code_id)