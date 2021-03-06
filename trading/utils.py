#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/16 13:25
# @Author   : Adolf
# @File     : utils.py
# @Function  :
import json
import requests
import logging


def post_msg_to_dingtalk(title="rich", msg="",
                         token="8392f247561974cf01f63efc77bfeb814c70a00453aee8eb26c405081af03dbe",
                         at=[], type="markdown"):
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + token
    if type == "markdown":
        # 使用markdown时at不起作用，大佬们有空调一下
        data = {"msgtype": "markdown",
                "markdown": {"title": "[" + title + "]" + title, "text": "" + msg},
                "at": {}
                }
    if type == "text":
        data = {"msgtype": "text",
                "text": {"content": "[" + title + "]" + title + "-" + msg},
                "at": {}
                }
    data["at"]["atMobiles"] = at
    json_data = json.dumps(data)
    try:
        response = requests.post(url=url, data=json_data, headers={"Content-Type": "application/json"}).json()
        assert response["errcode"] == 0
    except:
        logging.getLogger().error("发送钉钉提醒失败，请检查")


def get_balance_info(exchange):
    balance = exchange.fetch_balance()
    balance_my = dict()
    balance_my_value = 0
    max_value = 0

    for coin in balance["info"]["balances"]:
        if float(coin["free"]) + float(coin["locked"]) > 0:
            balance_my[coin["asset"]] = float(coin["free"]) + float(coin["locked"])
            if coin["asset"] == "USDT":
                balance_my_value += (float(coin["free"]) + float(coin["locked"]))
                if float(coin["free"]) + float(coin["locked"]) > max_value:
                    max_value = float(coin["free"]) + float(coin["locked"])
                    max_value_coin = "USDT"
            else:
                trick = exchange.fetch_ticker(symbol=coin["asset"] + "/USDT")
                balance_my_value += trick["ask"] * (float(coin["free"]) + float(coin["locked"]))
                if trick["ask"] * (float(coin["free"]) + float(coin["locked"])) > max_value:
                    max_value = trick["ask"] * (float(coin["free"]) + float(coin["locked"]))
                    max_value_coin = coin["asset"]

    return balance_my, max_value_coin, balance_my_value * 6.72
