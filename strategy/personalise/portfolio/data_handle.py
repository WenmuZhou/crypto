#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/7 15:21
# @Author   : Adolf
# @File     : data_handle.py
# @Function  :
import os
import pandas as pd

from functools import reduce

pd.set_option("expand_frame_repr", False)

stock_dir = "dataset/stock/stock_handle/"
stock_pool = os.listdir(stock_dir)
# print(stock_pool)

data_frames = []
for stock in stock_pool:
    # print(stock)
    stock_path = os.path.join(stock_dir, stock)
    stock_df = pd.read_csv(stock_path)
    stock_df["code"] = "stock_" + stock.split(".")[0]

    data_frames.append(stock_df)

# df_merged = reduce(lambda left, right: pd.merge(left, right, on=['date'],
#                                                 how='outer'), data_frames)
df_merged = pd.concat(data_frames)
df_merged.sort_values(by=['date'], inplace=True)

print(df_merged)
# df_merged.to_csv("dataset/stock/stock_merged.csv", index=False)

df2 = df_merged[df_merged['date'] > "2010-06-07"]
print(df2)
df2.to_csv("dataset/stock/stock_used.csv", index=False)
