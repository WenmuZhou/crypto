# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project : crypto
# @Date    : 2021/4/18 21:01
# @Author  : Adolf
# @File    : base_trading.py
# @Function:
import ccxt
import pandas as pd

import json
import requests
import logging
import datetime
from trading.UserInfo import api_key_dict, api_secret_dict


class BasisTrading:
    def __init__(self,
                 exchange_name="binance",
                 title="rich",
                 token="8392f247561974cf01f63efc77bfeb814c70a00453aee8eb26c405081af03dbe",
                 post_to_ding_talk=True):
        self.title = title
        self.token = token
        self.post_to_ding_talk = post_to_ding_talk

        if exchange_name == "binance":
            self.exchange = ccxt.binance()
        elif exchange_name == "huobi":
            self.exchange = ccxt.huobipro()

        # self.balance_my = None
        # self.max_value_coin = None
        # self.balance_my_value = None

    def get_data(self, coin_name, time_periods, data_limit):
        data = self.exchange.fetch_ohlcv(coin_name + "/USDT", timeframe=time_periods, limit=data_limit)
        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "vol"])

        return df

    @staticmethod
    def cal_technical_index(df, momentum_days=5):
        df["coin_pct"] = df["close"].pct_change(1)
        df["coin_mom"] = df["close"].pct_change(periods=momentum_days)
        return df

    def sell(self, pos_coin, balance_my):
        self.exchange.create_market_sell_order(symbol=pos_coin + "/USDT",
                                               amount=balance_my[pos_coin])

    def buy(self, overweight_pos, balance_my):
        trick = self.exchange.fetch_ticker(symbol=overweight_pos + "/USDT")
        self.exchange.create_limit_buy_order(symbol=overweight_pos + "/USDT", price=trick['ask'],
                                             amount=balance_my["USDT"] / trick['ask'])

    def strategy_trade(self, *args, **kwargs):
        # now_style = "USDT"
        # return now_style
        pass

    def trading_main(self, **kwargs):
        self.exchange.apiKey = api_key_dict[kwargs["user"]]
        self.exchange.secret = api_secret_dict[kwargs["user"]]

        balance_my, max_value_coin, balance_my_value = self.get_balance_info()

        now_style = self.strategy_trade(kwargs)
        if max_value_coin != now_style:
            if max_value_coin != "USDT":
                self.sell(max_value_coin, balance_my)
            if now_style != "USDT":
                self.buy(now_style, balance_my)

            message = "调仓时间:{}\n\n账户所有人:{}\n\n原来持有的币种:{}\n\n买入的新币种为:{}\n\n账户余额:{:.2f}元".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                kwargs["user"],
                max_value_coin, now_style, balance_my_value)
            if self.post_to_ding_talk:
                self.post_msg_to_dingtalk(
                    msg=message)
                print(message)
                print('---------')
        else:
            if self.post_to_ding_talk:
                print("账户所有人:", kwargs["user"])
                print("本次操作没有调仓")
                print('---------')

    def post_msg_to_dingtalk(self, msg="", at=[], type="markdown"):
        url = "https://oapi.dingtalk.com/robot/send?access_token=" + self.token
        if type == "markdown":
            # 使用markdown时at不起作用，大佬们有空调一下
            data = {"msgtype": "markdown",
                    "markdown": {"title": "[" + self.title + "]" + self.title, "text": "" + msg},
                    "at": {}
                    }
        if type == "text":
            data = {"msgtype": "text",
                    "text": {"content": "[" + self.title + "]" + self.title + "-" + msg},
                    "at": {}
                    }
        data["at"]["atMobiles"] = at
        json_data = json.dumps(data)
        try:
            response = requests.post(url=url, data=json_data, headers={"Content-Type": "application/json"}).json()
            assert response["errcode"] == 0
        except:
            logging.getLogger().error("发送钉钉提醒失败，请检查")

    def get_balance_info(self):
        balance = self.exchange.fetch_balance()
        balance_my = dict()
        balance_my_value = 0
        max_value = 0

        for coin in balance["info"]["balances"]:
            if float(coin["free"]) + float(coin["locked"]) > 0:
                # print(coin)
                balance_my[coin["asset"]] = float(coin["free"]) + float(coin["locked"])
                if coin["asset"] == "USDT":
                    balance_my_value += (float(coin["free"]) + float(coin["locked"]))
                    if float(coin["free"]) + float(coin["locked"]) > max_value:
                        max_value = float(coin["free"]) + float(coin["locked"])
                        max_value_coin = "USDT"
                else:
                    trick = self.exchange.fetch_ticker(symbol=coin["asset"] + "/USDT")
                    balance_my_value += trick["ask"] * (float(coin["free"]) + float(coin["locked"]))
                    if trick["ask"] * (float(coin["free"]) + float(coin["locked"])) > max_value:
                        max_value = trick["ask"] * (float(coin["free"]) + float(coin["locked"]))
                        max_value_coin = coin["asset"]

        return balance_my, max_value_coin, balance_my_value * 6.72
