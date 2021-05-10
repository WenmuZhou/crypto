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
try:
    auto_trade.trading_main(
        coin_list=["ONT", "WAVES", "KSM", "UNI", "CAKE", "BAKE", "FIL", "MATIC", "BCH", "LINK", "BAT", "LTC", "EOS"],
        user="wxt",
        time_periods="4h",
        momentum_days=5)
except Exception as e:
    print(e)
    print("wxt bug")

coin_list_ji = ["MATIC", "ANT", "OMG", "CHZ", "DOGE", "OMG", "CAKE", "ONT", "TLM", "BAKE", "CHR", "ETC", "XTZ", "SHIB"]
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

try:
    auto_trade.trading_main(coin_list=["DOT", "ADA", "BCH", "ETC"], user="zuol", time_periods="4h", momentum_days=10)
except Exception as e:
    print(e)
    print('zuol bug')

auto_trade_ma = TwoMATrade()
try:
    auto_trade_ma.trading_main(coin_name="REEF", long_ma=20, short_ma=5, user="feip", time_periods="4h")
except Exception as e:
    print(e)
    print('feip bug')
