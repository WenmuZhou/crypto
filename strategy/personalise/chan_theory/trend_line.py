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

# butch_femme_df = df[(df["flag"] == "b") | (df["flag"] == "f")]
flag_i = 0
for index, row in df.iterrows():
    if not pd.isnull(row["flag"]):
        df.loc[index, "flag_id"] = flag_i
        flag_i += 1

# print(df)
last_index = -5
for index, row in df.iterrows():
    # print(index, row)
    if not pd.isna(row["flag"]):
        if index - last_index < 5:
            if row["flag"] == "b":
                pre_high = df[df["flag_id"] == (row["flag_id"] - 2)].high.item()
                if row["flag_id"] > 1 and row["high"] > pre_high:
                    df.loc[last_index, "flag"] = "gan"
                    df.loc[df["flag_id"] == (row["flag_id"] - 2), "flag"] = "gan"
                    last_index = index
                else:
                    df.loc[index, "flag"] = "gan"

            if row["flag"] == "f":
                pre_low = df[df["flag_id"] == (row["flag_id"] - 2)].low.item()
                if row["flag_id"] > 1 and row["low"] < pre_low:
                    df.loc[last_index, "flag"] = "gan"
                    df.loc[df["flag_id"] == (row["flag_id"] - 2), "flag"] = "gan"
                    last_index = index
                else:
                    df.loc[index, "flag"] = "gan"
        else:
            last_index = index
    # break

# exit()
last_state = "p"
last_index = -1
for index, row in df.iterrows():
    if row["flag"] == "b" and row["flag"] == last_state:
        if df.loc[index, "high"] > df.loc[last_index, "high"]:
            df.loc[last_index, 'flag'] = "gan"
            last_index = index
        else:
            df.loc[index, 'flag'] = "gan"
    elif row["flag"] == "f" and row["flag"] == last_state:
        if df.loc[index, "low"] < df.loc[last_index, "low"]:
            df.loc[last_index, "flag"] = "gan"
            last_index = index
        else:
            df.loc[index, 'flag'] = "gan"
    elif row["flag"] == "b" or row["flag"] == "f":
        last_state = row["flag"]
        last_index = index
    else:
        continue
# # exit()
df.loc[df["flag"] == "b", "price"] = df["high"]
df.loc[df["flag"] == "f", "price"] = df["low"]

df2 = df.dropna(how="any")
print(df2)

l1 = plt.plot(df["date"], df["close"], 'r', label='close')
l2 = plt.plot(df2['date'], df2['price'], 'b', label='trend')
plt.plot(df["date"], df["close"], 'r', df2['date'], df2['price'], 'b')
# plt.savefig('result/test_trend.jpg')
plt.savefig("result/test_trend.svg", format="svg")
plt.show()
