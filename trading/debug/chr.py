#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/8 13:55
# @Author   : Adolf
# @File     : chr.py
# @Function  :
import ccxt
from trading.UserInfo import api_key_dict, api_secret_dict
from trading.utils import get_balance_info

exchange = ccxt.binance()

exchange.apiKey = api_key_dict["szq"]
exchange.secret = api_secret_dict["szq"]

balance_my, max_value_coin, balance_my_value = get_balance_info(exchange)

print(balance_my)
# trick = exchange.fetch_ticker(symbol="CHR/USDT")
# print(trick)
# exchange.create_limit_buy_order(symbol="CHR/USDT", price=trick['ask'],
#                                 amount=balance_my["USDT"] / trick['ask'])
