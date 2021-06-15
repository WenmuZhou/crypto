#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/15 16:08
# @Author   : Adolf
# @File     : analysis_mom.py
# @Function  :
import os.path

import pandas as pd

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

# df["slope_30"] = round(df["slope_30"], 1)
# df["mom_30"] = round(df["mom_30"], 2)
# temp = df.groupby('mom_30')['Day5Pct'].mean()
# temp = pd.DataFrame(temp)
# print(temp)
# print(df)

data_path = "/root/adolf/dataset/stock/handle_stock/mom"
data_list = os.listdir(data_path)
df_list = []
for data in data_list:
    df = pd.read_csv(os.path.join(data_path, data))
    df_list.append(df)
    # print(df)

df_concat = pd.concat(df_list, ignore_index=True)
df_concat = df_concat[df_concat["date"] > "2016-06-07"]
print(df_concat)
df_concat.to_csv("dataset/stock/mom_pool.csv", index=False)
