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


def post_msg_to_dingtalk(title="quant", msg="",
                         token="f0e92e8bb1c4d9c9d838f50b1c0fd627760f50121d551c26068d23086714bfaa",
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


def get_balance_info(coin_list, exchange):
    balance = exchange.fetch_balance()
    balance_my = dict()
    balance_my_value = 0
    max_value = 0

    for coin in balance["info"]["balances"]:
        if coin["asset"] in coin_list + ["USDT"]:
            balance_my[coin["asset"]] = float(coin["free"])
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
    print("how much money I have:", balance_my_value * 6.72)

    return balance_my, max_value_coin, balance_my_value
