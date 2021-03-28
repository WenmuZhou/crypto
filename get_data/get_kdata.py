# ！/usr/bin/env python
# -*- coding:utf-8 -*-
import ccxt
import pandas as pd

exchange = ccxt.binance()

exchange.apiKey = "e3cDWMh8N1uugwePjZK0OLZ73dMCl45kX7kIbniN9kjx42r5UtBAGs1S6JKvEXiu"
exchange.secret = "F6OShDNksFqTqCqD8mGbAEmi7sDubGWxHakra3nA8xVn3RWbw9qsDqNMi75OhNVG"

start_time = 1616016600000
time_diff = 899100000
res_data = []
for i in range(20):
    data = exchange.fetch_ohlcv("EOS/USDT", timeframe="15m", limit=1000, since=start_time-i*time_diff)
    res_data = data + res_data
print(res_data)
print(len(res_data))

df = pd.DataFrame(res_data, columns=["time_stamp", "open", "high", "low", "close", "vol"])
df['time_stamp'] = pd.to_datetime(df["time_stamp"], unit="ms")
df.to_csv("dataset/eos_15min.csv", index=False)
