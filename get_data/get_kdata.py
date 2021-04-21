# ！/usr/bin/env python
# -*- coding:utf-8 -*-
import ccxt
import os
import pandas as pd

exchange = ccxt.binance()

coin_list = ["BTC", "ETH", "EOS", "FIL", "LTC", "XRP", "DOT", "KSM", "CAKE", "BNB", "ADA", "UNI"]
time_period = "4h"
range_number = 10
limit_number = 1000


def get_exchange_data(coin_name):
    res_data = []
    for i in range(range_number):
        if len(res_data) == 0:
            data = exchange.fetch_ohlcv(coin_name + "/USDT", timeframe=time_period, limit=limit_number)
            # print('data len', len(data))
            time_dff = data[1][0] - data[0][0]
            # print(time_dff)
        else:
            # print(res_data)
            # print(len(res_data))
            st = res_data[0][0]
            # et = res_data[-1][0]
            # print('st', res_data[0][0])
            # print('et',res_data[-1][0])
            data = exchange.fetch_ohlcv(coin_name + "/USDT", timeframe=time_period, limit=limit_number,
                                        since=st - limit_number * time_dff)
        res_data = data + res_data
    # print(res_data)
    # print(len(res_data))
    df = pd.DataFrame(res_data, columns=["time", "open", "high", "low", "close", "vol"])
    df['time_stamp'] = pd.to_datetime(df["time"], unit="ms")
    # print(df)
    df.drop_duplicates(subset=['time_stamp'], inplace=True)
    print(len(df))
    data_dir = os.path.join("dataset", time_period)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    df.to_csv(os.path.join(data_dir, coin_name + ".csv"), index=False)


for coin_name_ in coin_list:
    get_exchange_data(coin_name_)
