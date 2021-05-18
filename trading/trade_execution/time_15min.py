#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/11 16:38
# @Author   : Adolf
# @File     : time_15min.py
# @Function  :
from trading.trade_strategy.two_ma import TwoMATrade
from trading.trade_strategy.turn_trade import TurnTrade

auto_trade_ma = TwoMATrade()
try:
    auto_trade_ma.trading_main(coin_name="REEF", long_ma=25, short_ma=7, user="feip", time_periods="15m")
except Exception as e:
    print(e)
    print('feip bug')

auto_trade = TurnTrade()
try:
    auto_trade.trading_main(coin_list=["EOS", "FIL", "LTC", "ETC", "BCH", "BAT", "BAKE", "XLM",
                                       "KSM", "CAKE", "LINK", "CHZ", "DOGE", "MATIC"],
                            user="zuol", time_periods="15m", momentum_days=96)
except Exception as e:
    print(e)
    print('zuol bug')
