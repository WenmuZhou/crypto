#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/9 16:50
# @Author   : Adolf
# @File     : analysis_two_ma.py
# @Function  :
import pandas as pd

pd.set_option("expand_frame_repr", False)

# print(df)
# print(df["is_win"].count())
# print(df.describe())
df = pd.read_csv("dataset/day/ETH.csv")
print(df)
