# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/5/30 14:56
# @Author  : Adolf
# @File    : range_regress.py
# @Function:
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

k1 = 0.3
k2 = 0.6
trade_rate = 2 / 1000

test_data = "dataset/5m/BTC_USDT_5m/from_2021-03-21_11-35-00_to_2021-05-29_22-10-00.csv"
df = pd.read_csv(test_data)
df = df[-1000:]
del df["time"]
df = df[["time_stamp", "open", "high", "low", "close"]]

df["coin_pct"] = df["close"].pct_change(1)
df['range'] = (df.high.rolling(2).max() - df.low.rolling(2).min()).shift(1)
df["long_open_price"] = df["open"] - k1 * df["range"]

df.dropna(how="any", inplace=True)
df.reset_index(drop=True, inplace=True)

holding = False
for index, row in df.iterrows():
    # print(row)
    if holding:
        if row["low"] < stop_loss_price:
            df.loc[index, "pct"] = stop_win_price / df.loc[index - 1, "close"] - 1
            df.loc[index, "pct"] = (1 + df.loc[index, "pct"]) * (1 - trade_rate) - 1
            holding = False
        elif row["high"] > stop_win_price:
            holding = False
            df.loc[index, "pct"] = max(row["open"], stop_win_price) / df.loc[index - 1, "close"] - 1
            df.loc[index, "pct"] = (1 + df.loc[index, "pct"]) * (1 - trade_rate) - 1
        else:
            df.loc[index, "pct"] = row["close"] / df.loc[index - 1, "close"] - 1

    else:
        if row["low"] < row["long_open_price"]:
            holding = True
            stop_win_price = row["long_open_price"] + k2 * row["range"]
            stop_loss_price = row["long_open_price"] - 200
            if row["low"] < stop_loss_price:
                df.loc[index, "pct"] = stop_win_price / row["long_open_price"] - 1
                df.loc[index, "pct"] = (1 + df.loc[index, "pct"]) * (1 - trade_rate) - 1
                holding = False
            else:
                df.loc[index, "pct"] = row["close"] / row["long_open_price"] - 1

        else:
            df.loc[index, "pct"] = 0

df["strategy_pct"] = (1 + df['pct']).cumprod()
df["coin_net"] = (1 + df["coin_pct"]).cumprod()
print(df)

plt.plot(df['time_stamp'], df["strategy_pct"], label="strategy_pct")
plt.plot(df["time_stamp"], df["coin_net"])
plt.show()
