#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/20 14:43
# @Author   : Adolf
# @File     : handle_data.py
# @Function  :
import pandas as pd

# pd.set_option("expand_frame_repr", False)

df = pd.read_csv("result/macd_threshold.csv")
df_col = df.columns.to_list()

for index, row in df.iterrows():
    best_odds = 0
    best_odds_params = 0
    for col in df_col:
        if "macd_odds_" in col:
            if row[col] > best_odds:
                best_odds = row[col]
                best_odds_params = col.replace("macd_odds_", "")
    df.loc[index, "best_odds_params"] = best_odds_params

print(df)
df.to_csv("result/macd_threshold_v2.csv")
