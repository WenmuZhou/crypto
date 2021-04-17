#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/14 10:42
# @Author   : Adolf
# @File     : turn_mul.py
# @Function  :
import ccxt
import pandas as pd
import datetime
from trading.utils import post_msg_to_dingtalk, get_balance_info
from trading.laboratory import api_key_dict, api_secret_dict

exchange = ccxt.binance()


def auto_trade(coin_list, user, time_periods="4h", momentum_days=5, msg_to_ding=True):
    exchange.apiKey = api_key_dict[user]
    exchange.secret = api_secret_dict[user]
    balance_my, max_value_coin, balance_my_value = get_balance_info(coin_list, exchange)

    coin_mom = {}
    for coin_name in coin_list:
        data = exchange.fetch_ohlcv(coin_name + "/USDT", timeframe=time_periods, limit=30)
        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "vol"])

        df['coin_pct'] = df['close'].pct_change(1)
        df['coin_mom'] = df['close'].pct_change(periods=momentum_days)
        # print(df)
        # print(df.tail(1)["coin_mom"].item())
        coin_mom[coin_name] = df.tail(1)["coin_mom"].item()

    max_value = max(coin_mom.values())
    for keys, values in coin_mom.items():
        if values == max_value:
            # print(keys, values)
            now_style = keys
            if max_value <= 0:
                now_style = "USDT"

    print("origin balance:", balance_my)
    print("origin position:", max_value_coin)

    print("now_style:", now_style)
    max_value_coin_new = max_value_coin
    if max_value_coin != now_style:
        if max_value_coin_new != "USDT":
            # trick = exchange.fetch_ticker(symbol=max_value_coin + "/USDT")
            exchange.create_market_sell_order(symbol=max_value_coin + "/USDT",
                                              amount=balance_my[max_value_coin])
            # balance_my_new, max_value_coin_new, balance_my_value = get_balance_info(coin_list, exchange)

        if now_style != "USDT":
            trick = exchange.fetch_ticker(symbol=now_style + "/USDT")
            exchange.create_limit_buy_order(symbol=now_style + "/USDT", price=trick['ask'],
                                            amount=balance_my["USDT"] / trick['ask'])

    balance_my_new, max_value_coin_new, balance_my_value = get_balance_info(coin_list, exchange)
    if max_value_coin_new == max_value_coin:
        msg_to_ding = False
    if msg_to_ding:
        post_msg_to_dingtalk(
            msg="调仓时间:{}\n\n账户所有人:{}\n\n原来持有的币种:{}\n\n买入的新币种为:{}\n\n账户余额:{:.2f}元".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user,
                max_value_coin, max_value_coin_new, balance_my_value))


coin_list_1 = ["EOS", "ANT", "DOT", "CHZ", "ADA", "UNI", "DOGE", "FIL", "CAKE", "ONT", "TLM", "BNB"]
auto_trade(coin_list_1, user="wenmu", msg_to_ding=True)

# coin_list_2 = ["BTC","ETH","ADA","UNI","FIL"]
# auto_trade(coin_list_2,user="wxt")
