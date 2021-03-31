# ！/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
import talib

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)

df = pd.read_csv("dataset/day/BTC.csv")
del df['high'], df['low'], df['vol']

for i in [1, 3, 5, 10, 20, 30]:
    df[str(i) + 'day_pct'] = df['close'].pct_change(i)
    df[str(i) + 'day_pct'] = df[str(i) + 'day_pct'].shift(-i)

for i in [5, 10, 20, 30, 60]:
    df[str(i) + '_ma'] = talib.SMA(df["close"], timeperiod=i)
    # df['3day_pct'] = df['close'].pct_change(3)
# df.dropna(subset=['1day_pct'],inplace=True)
df = df.dropna(how="any")
df.reset_index(drop=True, inplace=True)
df["sum_pct"] = df.loc[df["close"] > df["5_ma"], "1day_pct"]
tmp_df = df.dropna(how="any")
mean_df = tmp_df.mean(axis=0)
print(mean_df)
# sum_pct = tmp_df.loc[len(tmp_df)-1,"sum_pct"]
# print(tmp_df)
