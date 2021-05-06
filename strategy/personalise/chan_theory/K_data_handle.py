#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/6 10:46
# @Author   : Adolf
# @File     : K_data_handle.py
# @Function  :
import pandas as pd

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

df = pd.read_csv("dataset/stock/sh.600570.csv")
df = df[-1000:]
# print(df)
# exit()
# print(df[:10])

get_merge_data = []
for index, row in df.iterrows():
    if len(get_merge_data) == 0:
        get_merge_data.append([row['date'], row["high"], row["low"]])
    else:
        _, pre_high, pre_low = get_merge_data[-1]
        # print(pre_high, pre_low)
        if (row["high"] >= pre_high and row["low"] <= pre_low) or (row["high"] <= pre_high and row["low"] >= pre_low):
            _, pre_plus_high, pre_plus_low = get_merge_data[-2]
            get_merge_data.pop()
            if pre_high > pre_plus_high:
                now_high = max(row["high"], pre_high)
                now_low = max(row["low"], pre_low)
            else:
                now_high = min(row["high"], pre_high)
                now_low = min(row["low"], pre_low)
        # elif row["high"] <= pre_high and row["low"] >= pre_low:
        #     _, pre_plus_high, pre_plus_low = get_merge_data[-2]
        #     get_merge_data.pop()
        #     if pre_high > pre_plus_high:
        #         now_high = max(row["high"], pre_high)
        #         now_low = max(row["low"], pre_low)
        #     else:
        #         now_high = min(row["high"], pre_high)
        #         now_low = min(row["low"], pre_low)
        else:
            now_high = row["high"]
            now_low = row["low"]
        get_merge_data.append([row['date'], now_high, now_low])

    # if index > 10:
    #     break

# print(len(df))
# print(len(get_merge_data))
# print(get_merge_data)
