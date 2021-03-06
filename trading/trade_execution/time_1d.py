#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/19 17:18
# @Author   : Adolf
# @File     : time_1d.py
# @Function  :
from trading.trade_strategy.turn_trade import TurnTrade
from trading.trade_strategy.turtle_trade import TurtleTrade

auto_trade = TurnTrade()
# try:
#     auto_trade.trading_main(coin_list=["BTC", "ETH", "UNI", "FIL", "DOT", "ADA"], user="nan",
#                             time_periods="1d",
#                             momentum_days=5)
# except Exception as e:
#     print(e)
#     print('nan bug')

# try:
#     auto_trade.trading_main(coin_list=["BTC", "ETH", "ADA", "DOT", "UNI", "BNB"], user="wxt", time_periods="1d",
#                             momentum_days=60)
# except Exception as e:
#     print(e)
#     print("wxt bug")

try:
    auto_trade.trading_main(coin_list=["BTC", "ETH", "BNB", "UNI"], user="shengl",
                            time_periods="1d",
                            momentum_days=10)
except Exception as e:
    print(e)
    print('shengl bug')

try:
    auto_trade.trading_main(coin_list=["BTC", "ETH", "BNB", "UNI"], user="wyy",
                            time_periods="1d",
                            momentum_days=20)
except Exception as e:
    print(e)
    print('wyy bug')

auto_trade_v2 = TurtleTrade()
try:
    auto_trade_v2.trading_main(coin_name="BTC", user="yujl", upper_band=20, lower_band=10, time_periods="1d")
except Exception as e:
    print(e)
    print('yujl bug')
