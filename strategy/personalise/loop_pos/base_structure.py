#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/24 14:13
# @Author   : Adolf
# @File     : base_structure.py
# @Function  :
import pandas as pd
import json


class TradeStructure:
    def __init__(self, data_path):
        self.position = self.init_position()
        self.data = self.load_dataset(data_path)
        self.trade_rate = 1 / 1000
        self.pos_tracking = []

    @staticmethod
    def init_position():
        return {
            "date": "",
            "pre_pos": 1,
            "pre_price": "cash",
            "pos_price": 1,
            "pos_style": "cash",
            "value": 1,
            "is_turn": False}

    @staticmethod
    def init_one_pos_record():
        return {"pos_asset": "stock",
                "buy_date": "",
                "buy_price": 1,
                "sell_date": "",
                "sell_price": 1,
                "holding_time": 0}

    @staticmethod
    def load_dataset(_data_path, start_stamp="", end_stamp=""):
        df = pd.read_csv(_data_path)
        try:
            df = df[['date', 'open', 'close', 'high', 'low', 'volume']]
        except Exception as e:
            print(e)
            df = df[['DATES', 'open', 'close', 'high', 'low', 'volume']]
            df = df.rename(columns={"DATES": "date"})
        # print(df)
        df['trade'] = ""
        df = df[-1000:]
        return df

    def cal_technical_index(self):
        self.data["MA5"] = self.data["close"].rolling(5).mean()
        self.data['MA10'] = self.data["close"].rolling(10).mean()

    def buy(self, buy_asset="stock", buy_price=1):
        self.position["pos_style"] = buy_asset
        self.position["pos_price"] = buy_price
        self.position['value'] *= (1 - self.trade_rate)

    def sell(self, sell_asset="stock", sell_price=1):
        self.position["pos_style"] = "cash"
        self.position["pos_price"] = 1
        self.position["value"] *= (1 + sell_price / self.position["pre_price"])
        self.position['value'] *= (1 - self.trade_rate)

    def strategy_exec(self):
        # self.data.to_csv("result/test_base.csv")
        one_pos_record = self.init_one_pos_record()
        for index, row in self.data.iterrows():
            self.position["pre_style"] = self.position["pos_style"]
            self.position["pre_price"] = self.position["pos_price"]
            if row["trade"] == "buy":
                self.buy(buy_price=row["close"])
                one_pos_record["buy_date"] = row["date"]
                one_pos_record["buy_price"] = row["close"]
                one_pos_record["holding_time"] = -index
            if row["trade"] == "sell" and one_pos_record["buy_date"] != "":
                self.sell(sell_price=row["close"])
                one_pos_record["sell_date"] = row["date"]
                one_pos_record["sell_price"] = row["close"]
                # print('one_pos_record["holding_time"]:', one_pos_record["holding_time"])
                # print("index:", index)
                # print("=" * 20)
                one_pos_record["holding_time"] += index
                self.pos_tracking.append(one_pos_record.copy())
                one_pos_record = self.init_one_pos_record()
            else:
                self.position["pos_style"] = self.position["pre_style"]
                self.position["pos_price"] = row["close"]
                self.position["value"] *= (1 + self.position["pos_price"] / self.position["pre_price"])

    def eval_index(self):
        eval_df = pd.DataFrame(self.pos_tracking)
        eval_df["pct"] = (eval_df["sell_price"] / eval_df["buy_price"]) - 1
        eval_df['strategy_net'] = (1 + eval_df['pct']).cumprod()
        eval_df["pct_show"] = eval_df["pct"].apply(lambda x: format(x, '.2%'))
        print(eval_df)

        print("策略成功率:{:.2f}%".format(len(eval_df[eval_df["pct"] > 0]) / len(eval_df) * 100))
        print("策略赔率:{:.2f}%".format(eval_df["pct"].mean() * 100))

    def __call__(self, show_buy_and_sell=False, analyze_positions=False):
        self.cal_technical_index()
        if show_buy_and_sell:
            res_list = []
            data_dict = {}
            item_list = ["date", "open", "close", "low", "high", "volume", "trade"]
            for index, row in self.data.iterrows():
                for item in item_list:
                    data_dict[item] = row[item]
                res_list.append(data_dict.copy())
            return json.dumps(res_list, indent=2, ensure_ascii=False)
        self.strategy_exec()
        if analyze_positions:
            self.eval_index()
