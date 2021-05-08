#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/8 13:44
# @Author   : Adolf
# @File     : trend_line.py
# @Function  :
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

df = pd.read_csv("result/hs_stock.csv")
del df['amount'], df['turn'], df['pctChg'], df['adjustflag']

last_index = -1
for index, row in df.iterrows():
    if not pd.isnull(row['flag']):
        if index - last_index < 5:
            df.loc[index, 'flag'] = "gan"
        last_index = index

last_state = "p"
last_index = -1
for index, row in df.iterrows():
    if row["flag"] == "b" or row["flag"] == "f":
        if row["flag"] == last_state:
            # df.loc[index, 'flag'] = "gan"

# exit()
df.loc[df["flag"] == "b", "price"] = df["high"]
df.loc[df["flag"] == "f", "price"] = df["low"]

df2 = df.dropna(how="any")
print(df2)

l1 = plt.plot(df["date"], df["close"], 'r', label='close')
l2 = plt.plot(df2['date'], df2['price'], 'b', label='trend')
plt.plot(df["date"], df["close"], 'r', df2['date'], df2['price'], 'b')
# plt.savefig('result/test_trend.jpg')
plt.show()
