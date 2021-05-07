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
        coin_list=["BTC", "ETH", "BNB", "DOT", "KSM", "UNI", "CAKE", "BAKE", "FIL", "FLOW", "MATIC", "XRP", "BCH",
                   "LINK", "BAT"],
        user="wxt",
        time_periods="4h",
        momentum_days=5)
except Exception as e:
    print(e)
    print("wxt bug")
try:
    auto_trade.trading_main(
        coin_list=["MATIC", "ANT", "DOT", "CHZ", "DOGE", "FIL", "CAKE", "ONT", "TLM", "BAKE", "CHR"],
        user="wenmu",
        time_periods="4h", momentum_days=5)
except Exception as e:
    print(e)
    print('wenmu bug')

try:
    auto_trade.trading_main(coin_list=["DOT", "ADA", "BCH", "ETC"], user="zuol", time_periods="4h", momentum_days=60)
except Exception as e:
    print(e)
    print('zuol bug')

auto_trade_ma = TwoMATrade()
try:
    auto_trade_ma.trading_main(coin_name="REEF", long_ma=25, short_ma=8, user="feip", time_periods="4h")
except Exception as e:
    print(e)
    print('feip bug')
