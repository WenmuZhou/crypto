#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/6 9:58
# @Author  : Adolf
# @File    : two_ma_pro.py
import os
import talib
import pandas as pd

df = pd.read_csv("dataset/day/LTC.csv")

df["ma_short"] = talib.SMA(df["close"], timeperiod=7)
df["ma_long"] = talib.SMA(df["close"], timeperiod=25)

df[(df["long_ma"]<df["ma_short"])]