#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/19 17:17
# @Author   : Adolf
# @File     : time_4h.py
# @Function  :
from trading.trade_strategy.turn_trade import TurnTrade

auto_trade = TurnTrade()
try:
    auto_trade.trading_main(
        coin_list=["DOT", "KSM", "UNI", "CAKE", "BAKE", "FIL", "MATIC", "BCH", "LINK", "BAT", "LTC", "EOS", "DOGE"],
        user="wxt",
        time_periods="4h",
        momentum_days=5)
except Exception as e:
    print(e)
    print("wxt bug")

coin_list_ji = ["MATIC", "ANT", "OMG", "CHZ", "DOGE", "XLM", "CAKE", "ONT", "TLM", "BAKE", "ETC", "XTZ"]
try:
    auto_trade.trading_main(
        coin_list=coin_list_ji,
        user="wenmu",
        time_periods="4h", momentum_days=5)
except Exception as e:
    print(e)
    print('wenmu bug')

try:
    auto_trade.trading_main(
        coin_list=coin_list_ji,
        user="shuig",
        time_periods="4h", momentum_days=5)
except Exception as e:
    print(e)
    print('shuig bug')

try:
    auto_trade.trading_main(
        coin_list=coin_list_ji,
        user="szq",
        time_periods="4h", momentum_days=5)
except Exception as e:
    print(e)
    print('szq bug')
