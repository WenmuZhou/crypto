#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/1 15:13
# @Author  : Adolf
# @File    : s_2b.py
import pandas as pd

df = pd.read_csv("result/牛熊分割线熊市买入.csv", encoding="gbk")

# print(df)
tmp_dict = dict()
for index, row in df.iterrows():
    # print(row)
    tmp_key = row["币名"] + "/" + row["周期线"]
    if tmp_key not in tmp_dict:
        tmp_dict[tmp_key] = {}

    tmp_dict[tmp_key][row["时间"]] = row["回报率"]
    # break

print(tmp_dict)

df2 = pd.DataFrame(tmp_dict).T
print(df2)
df2.to_csv("result/牛熊分割线熊市买入.csv", encoding="gbk")