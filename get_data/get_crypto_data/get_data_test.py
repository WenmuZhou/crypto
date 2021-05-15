#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/13 15:26
# @Author   : Adolf
# @File     : get_data_test.py
# @Function  :
import ccxt
from get_data.get_crypto_data.DownloadDataFromBinance import get_exchange_data

exchange_handler = ccxt.binance()
coin_name = "DOT"
time_period = "4h"
range_number = 2
storage_path = "dataset/test/"
limit = 1000

get_exchange_data(_exchange_handler=exchange_handler, _coin_name=coin_name, _time_period=time_period,
                  _range_number=range_number, _storage_path=storage_path, _limit=limit, _retry_times=3)
