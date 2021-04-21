#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/31 16:51
# @Author  : Adolf
# @File    : view_data.py
import ccxt
import pandas as pd
import talib
import mplfinance as mpf

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

exchange = ccxt.binance()

data = exchange.fetch_ohlcv("ETH/USDT", timeframe="1d", limit=100)
df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "volume"])

df["ma_long"] = talib.SMA(df["close"], timeperiod=10)
df["ma_short"] = talib.SMA(df["close"], timeperiod=7)
# df.set_index(["time"],inplace=True)
df['Date'] = pd.to_datetime(df["time"], unit="ms")
df.set_index('Date', inplace=True)
print(df)

my_color = mpf.make_marketcolors(up="red", down="green", edge="inherit", volume="inherit")
my_style = mpf.make_mpf_style(marketcolors=my_color)

# add_plot = [mpf.make_addplot(df[['ma_short', 'ma_long']])]
# add_plot = [mpf.make_addplot(df[['ma5', 'ma10']]),
#             mpf.make_addplot(df['signal_long'], scatter=True, makersize=80, marker="^", color="r"),
#             mpf.make_addplot(df['signal_short'], scatter=True, makersize=80, marker="v", color="g"),
#             mpf.make_addplot(df['signal_0'], scatter=True, makersize=80, color="y")]
# mpf.plot(df, type="candle", ylabel="price(usdt)", style=my_style, volume=True, ylabel_lower="vol",
# addplot=add_plot)
mpf.plot(df)
