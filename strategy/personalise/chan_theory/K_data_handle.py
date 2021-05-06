#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/6 10:46
# @Author   : Adolf
# @File     : K_data_handle.py
# @Function  :
import pandas as pd

df = pd.read_csv("/root/adolf/dataset/d_pre/sh.600570.csv")
# print(df)

get_merge_data = []
for index, row in df.iterrows():
    if len(get_merge_data) == 0:
        get_merge_data.append([row["high"], row["low"]])
    print(row)
    break
