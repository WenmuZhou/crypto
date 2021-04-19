#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/19 17:17
# @Author   : Adolf
# @File     : time_4h.py
# @Function  :
from trading.trade_strategy.turn_trade import TurnTrade

auto_trade = TurnTrade()
auto_trade.trading_main(coin_list=["BTC", "ETH", "ADA", "DOT", "ONT", "UNI", "BNB"], user="wxt", time_periods="4h",
                        momentum_days=5)

auto_trade.trading_main(
    coin_list=["EOS", "ANT", "DOT", "CHZ", "ADA", "UNI", "DOGE", "FIL", "CAKE", "ONT", "TLM", "BNB"], user="wenmu",
    time_periods="4h", momentum_days=5)
auto_trade.trading_main(coin_list=["DOT", "ADA"], user="zuol", time_periods="4h", momentum_days=5)
