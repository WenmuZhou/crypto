#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/13 15:26
# @Author   : Adolf
# @File     : get_data_test.py
# @Function  :
import ccxt
from get_data.get_crypto_data.DownloadDataFromBinance import get_exchange_data

exchange = ccxt.binance()

proxies = {
    'http': "http://172.17.45.65:1087",
    'https': "http://172.17.45.65:1087",
}

exchange.proxies = proxies
# coin_name = "DOT"
coin_list = ["BTC", "ETH", "EOS", "FIL", "LTC", "ETC", "BCH", "BAT",
             "XRP", "DOT", "KSM", "CAKE", "BNB", "LINK", "ADA", "UNI",
             "CHZ", "DOGE", "MATIC"]
time_period = "1m"
range_number = 10
storage_path = "dataset/" + time_period + "/"
limit = 1000

for coin_name in coin_list:
    get_exchange_data(_exchange_handler=exchange, _coin_name=coin_name, _time_period=time_period,
                      _range_number=range_number, _storage_path=storage_path, _limit=limit, _retry_times=3)
    # break
