#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/15 14:10
# @Author   : Adolf
# @File     : laboratory.py
# @Function  :
import ccxt

exchange = ccxt.binance()

# me
# exchange.apiKey = "e3cDWMh8N1uugwePjZK0OLZ73dMCl45kX7kIbniN9kjx42r5UtBAGs1S6JKvEXiu"
# exchange.secret = "F6OShDNksFqTqCqD8mGbAEmi7sDubGWxHakra3nA8xVn3RWbw9qsDqNMi75OhNVG"

# huobi
# exchange.apiKey = "36d91f66-64ad504e-rfhfg2mkl3-4a951"
# exchange.secret = "65c87438-5cead1d6-3e7271af-69f77"

api_key_dict = {
    "nan": "e3cDWMh8N1uugwePjZK0OLZ73dMCl45kX7kIbniN9kjx42r5UtBAGs1S6JKvEXiu",
    "wenmu": "J0p53QWHzOaU6h7ZmmGukFfJ7C97tN3rhhs7s3jFmZJ2rNHZvxYvoYDHklMrWWZq",
    "yujl": "b1hTOVS08l5Lk9O7BjqcIvbUURnIIbFQA9CtjPGFPaYM4Yz2xNzQ3UPs0nbcR1c0",
}
api_secret_dict = {
    "nan": "F6OShDNksFqTqCqD8mGbAEmi7sDubGWxHakra3nA8xVn3RWbw9qsDqNMi75OhNVG",
    "wenmu": "0MOMZJC3fNW0FsDL5Xu3qj2YNK8dPVqDgbxqR3USCi396uy1aCXxW2Tto78nuGWA",
    "yujl": "ehFJFU8xZgnfSdVCFZAGbyQWGsK94pKvoRlOJBmiG19MK4VOHFhWK1PbIBLwtYna"
}
