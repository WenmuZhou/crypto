#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/29 10:43
# @Author   : Adolf
# @File     : shui_buy.py
# @Function  :
import ccxt
from trading.utils import get_balance_info
from trading.UserInfo import api_key_dict, api_secret_dict

exchange = ccxt.binance()

exchange.apiKey = api_key_dict["shuig"]
exchange.secret = api_secret_dict["shuig"]

balance_my, max_value_coin, balance_my_value = get_balance_info(exchange)
print(balance_my)
