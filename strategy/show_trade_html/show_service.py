#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/23 12:23
# @Author   : Adolf
# @File     : show_service.py
# @Function  :
import json
from flask import Flask
from flask import request
import traceback
from flask_cors import CORS
from strategy.show_trade_html.parse_show_data import parse_data

"""
support 股票展示服务
"""
app = Flask(__name__)
CORS(app, resources=r'/*')


def request_parse(req_data):
    '''解析请求数据并以json形式返回'''
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


@app.route('/show_stock_data/', methods=["post", "get"], strict_slashes=False)
def service_main():
    try:
        data = request_parse(request)
        if data is not None:
            stock_id = data.get("stock_id")
            level = data.get("level")
            # ma1 = data.get("ma1")
            # ma2 = data.get("ma2")
            # ma3 = data.get("ma3")

            result = parse_data(stock_id=stock_id, level=level)
            # result_dict['result'] = result
            return result

            # return json.dumps(result)
        else:
            return json.dumps({"error_msg": "data is None", "status": 1}, ensure_ascii=False)
    except Exception as e:
        traceback.print_exc()
        return json.dumps({"error_msg": "unknown error:" + repr(e), "status": 1}, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
