# ！/usr/bin/env python
# -*- coding:utf-8 -*-
import ccxt
import pandas as pd

exchange = ccxt.binance()

# exchange.apiKey = "e3cDWMh8N1uugwePjZK0OLZ73dMCl45kX7kIbniN9kjx42r5UtBAGs1S6JKvEXiu"
# exchange.secret = "F6OShDNksFqTqCqD8mGbAEmi7sDubGWxHakra3nA8xVn3RWbw9qsDqNMi75OhNVG"
#
coin_list = ["BTC", "ETH", "EOS", "FIL", "LTC", "XRP", "DOT", "FIL", "KSM", "CAKE", "BNB", "ADA", "UNI"]
time_period = "1h"


# coin_list = ["BTC"]


# start_time = 1616016600000
# time_diff = 899100000
def get_exchange_data(coin_name):
    res_data = []
    for i in range(10):
        if len(res_data) == 0:
            data = exchange.fetch_ohlcv(coin_name + "/USDT", timeframe=time_period, limit=1000)
            time_dff = data[-1][0] - data[0][0]
        else:
            st = res_data[0][0]
            # et = res_data[-1][0]
            # print('st',res_data[0][0])
            # print('et',res_data[-1][0])
            data = exchange.fetch_ohlcv(coin_name + "/USDT", timeframe=time_period, limit=1000, since=st - time_dff)
        res_data = data + res_data
    # print(res_data)
    print(len(res_data))
    df = pd.DataFrame(res_data, columns=["time", "open", "high", "low", "close", "vol"])
    df['time_stamp'] = pd.to_datetime(df["time"], unit="ms")
    print(df)
    df.drop_duplicates(subset=['time_stamp'], inplace=True)
    df.to_csv("dataset/1hour/" + coin_name + ".csv", index=False)


for coin_name_ in coin_list:
    get_exchange_data(coin_name_)
