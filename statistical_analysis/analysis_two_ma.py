#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/9 16:50
# @Author   : Adolf
# @File     : analysis_two_ma.py
# @Function  :
import pandas as pd

df = pd.read_csv("result/two_ma_pro.csv")

# print(df)
# print(df["is_win"].count())
print(df.describe())
