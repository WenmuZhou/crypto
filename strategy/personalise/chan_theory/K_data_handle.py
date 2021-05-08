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
one_k_info = {"high_date": "",
              "low_date": "",
              "high_value": "",
              "low_value": "", }
for index, row in df.iterrows():
    if len(get_merge_data) == 0:
        one_k_info["high_date"] = row["date"]
        one_k_info["low_date"] = row["date"]
        one_k_info["high_value"] = row["high"]
        one_k_info["low_value"] = row["low"]
        get_merge_data.append(one_k_info.copy())
    else:
        pre_dict = get_merge_data[-1]
        pre_high = pre_dict["high_value"]
        pre_low = pre_dict["low_value"]
        pre_high_date = pre_dict["high_date"]
        pre_low_date = pre_dict["low_value"]
        # print(pre_high, pre_low)
        if (row["high"] >= pre_high and row["low"] <= pre_low) or (row["high"] <= pre_high and row["low"] >= pre_low):
            pre_plus_dict = get_merge_data[-2]
            pre_plus_high = pre_plus_dict["high_value"]
            get_merge_data.pop()
            if pre_high > pre_plus_high:
                now_high = max(row["high"], pre_high)
                now_low = max(row["low"], pre_low)
            else:
                now_high = min(row["high"], pre_high)
                now_low = min(row["low"], pre_low)

            if now_high == row["high"]:
                now_high_date = row["date"]
            else:
                now_high_date = pre_high_date

            if now_low == row["low"]:
                now_low_date = row["date"]
            else:
                now_low_date = pre_low_date
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
            now_high_date = row["date"]
            now_low_data = row["date"]

        one_k_info["high_date"] = now_high_date
        one_k_info["low_date"] = now_low_data
        one_k_info["high_value"] = now_high
        one_k_info["low_value"] = now_low
        # print(one_k_info)
        # print(get_merge_data)
        get_merge_data.append(one_k_info.copy())

    # if index > 10:
    #     break

# print(len(df))
# print(len(get_merge_data))
# print(get_merge_data)
