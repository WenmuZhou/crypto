#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/17 16:32
# @Author   : Adolf
# @File     : chan_zs.py
# @Function  :
import pandas as pd

pd.set_option("expand_frame_repr", False)

df = pd.read_csv("result/chan_600570.csv")

df2 = df.dropna(how="any")
df2.reset_index(inplace=True)
# print(df2)

interval_list = []
for index, row in df2.iterrows():
    if row["flag_bf"] == "b":
        flag_direction = "up"
    else:
        flag_direction = "down"
    # print(row)
    if index == 0:
        if flag_direction == "down":
            interval_list.append([[df.loc[0, "high"], row["price"]], flag_direction])
        else:
            interval_list.append([[df.loc[0, "low"], row["price"]], flag_direction])
    else:
        interval_list.append([[df2.loc[index - 1, "price"], row["price"]], flag_direction])

print(interval_list)
for interval_index in range(1, len(interval_list)):
    print(interval_list[interval_index])
    break
