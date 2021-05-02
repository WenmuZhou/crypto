#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/19 17:17
# @Author   : Adolf
# @File     : time_4h.py
# @Function  :
from trading.trade_strategy.turn_trade import TurnTrade
from trading.trade_strategy.two_ma import TwoMATrade

auto_trade = TurnTrade()
# try:
#     auto_trade.trading_main(coin_list=["BTC", "ETH", "ADA", "DOT", "UNI", "BNB"], user="wxt", time_periods="4h",
#                             momentum_days=5)
# except Exception as e:
#     print(e)
#     print("wxt bug")
try:
    auto_trade.trading_main(
        coin_list=["EOS", "ANT", "DOT", "CHZ", "ADA", "UNI", "DOGE", "FIL", "CAKE", "ONT", "TLM", "BAKE"], user="wenmu",
        time_periods="4h", momentum_days=5)
except Exception as e:
    print(e)
    print('wenmu bug')

try:
    auto_trade.trading_main(coin_list=["DOT", "ADA"], user="zuol", time_periods="4h", momentum_days=120)
except Exception as e:
    print(e)
    print('zuol bug')

auto_trade_ma = TwoMATrade()
try:
    auto_trade_ma.trading_main(coin_name="REEF", long_ma=25, short_ma=8, user="feip", time_periods="4h")
except Exception as e:
    print(e)
    print('feip bug')
A
