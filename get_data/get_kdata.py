# ！/usr/bin/env python
# -*- coding:utf-8 -*-
import ccxt
import pandas as pd

exchange = ccxt.binance()

# exchange.apiKey = "e3cDWMh8N1uugwePjZK0OLZ73dMCl45kX7kIbniN9kjx42r5UtBAGs1S6JKvEXiu"
# exchange.secret = "F6OShDNksFqTqCqD8mGbAEmi7sDubGWxHakra3nA8xVn3RWbw9qsDqNMi75OhNVG"
#
coin_list = ["BTC", "ETH", "EOS", "FIL", "LTC", "XRP", "DOT", "FIL", "KSM", "CAKE"]


# start_time = 1616016600000
# time_diff = 899100000
def get_exchange_data(coin_name):
    res_data = []
    for i in range(20):
        data = exchange.fetch_ohlcv(coin_name + "/USDT", timeframe="30m", limit=1000)
        res_data = data + res_data
    # print(res_data)
    print(len(res_data))
    df = pd.DataFrame(res_data, columns=["time", "open", "high", "low", "close", "vol"])
    df['time_stamp'] = pd.to_datetime(df["time"], unit="ms")
    df.to_csv("dataset/30min/" + coin_name + ".csv", index=False)


for coin_name_ in coin_list:
    get_exchange_data(coin_name_)
