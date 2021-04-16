#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/16 13:50
# @Author   : Adolf
# @File     : balance_inquire.py
# @Function  :
import ccxt
from trading.utils import get_balance_info, post_msg_to_dingtalk
import datetime

exchange = ccxt.binance()

coin_list = ["BTC", "ETH", "EOS", "XRP", "DOT", "BNB", "ADA", "UNI"]

api_key_dict = \
    {"wenmu": "J0p53QWHzOaU6h7ZmmGukFfJ7C97tN3rhhs7s3jFmZJ2rNHZvxYvoYDHklMrWWZq"}
api_secret_dict = \
    {"wenmu": "0MOMZJC3fNW0FsDL5Xu3qj2YNK8dPVqDgbxqR3USCi396uy1aCXxW2Tto78nuGWA"}

for api_name, api_key in api_key_dict.items():
    api_secret = api_secret_dict[api_name]
    exchange.apiKey = api_key
    exchange.secret = api_secret

    balance_my, max_value_coin, balance_my_value = get_balance_info(coin_list, exchange)

    post_msg_to_dingtalk(title="rich", msg="当前时间：{},账户所有人：{},账户余额：{}".format(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        api_name, balance_my_value * 6.72),
                         token="8392f247561974cf01f63efc77bfeb814c70a00453aee8eb26c405081af03dbe")

