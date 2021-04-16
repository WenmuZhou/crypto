#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/16 16:56
# @Author   : Adolf
# @File     : turtle.py
# @Function  :
import talib
import pandas as pd
import numpy as np
import mplfinance as mpf

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

df = pd.read_csv("dataset/1d/BTC.csv")
# print(df)

df['upper_band'] = talib.MAX(df.high, timeperiod=20).shift(1)
df['lower_band'] = talib.MIN(df.low, timeperiod=20).shift(1)
# df['upper_band'] = df["upper_band"].shift(-1)
# df['lower_band'] = df["lower_band"].shift(-1)


# df["Date"] = df["time_stamp"]
# df.rename(columns={"time_stamp": "Date", "vol": "volume"}, inplace=True)
#
# df.set_index("Date", inplace=True)
# df.index = pd.to_datetime(df.index)

df.loc[df["close"] > df["upper_band"], "style"] = "BTC"
df.loc[df['close'] < df["lower_band"], "style"] = "empty"

df['coin_pct'] = df['close'].pct_change(periods=1)

df["pos"] = df["style"].shift(1)
df["pos"] = df["pos"].fillna(method='pad')

df.dropna(inplace=True)
del df["style"]
# df.loc[df['pos'] != df['pos'].shift(1), 'trade_time'] = df["time_stamp"]
# df.loc[df["pos"]=="BTC","strategy_pct"] = df["coin_pct"]


# my_color = mpf.make_marketcolors(up="red", down="green", edge="inherit", volume="inherit")
# my_style = mpf.make_mpf_style(marketcolors=my_color)

# add_plot = [mpf.make_addplot(df[['upper_band', 'lower_band']])]
# mpf.plot(df, type="candle", ylabel="price(usdt)", style=my_style,addplot=add_plot)
print(df)
# df.to_csv("tmp/test2.csv", index=False)
