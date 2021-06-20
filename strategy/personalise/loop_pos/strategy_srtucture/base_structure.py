#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/24 14:13
# @Author   : Adolf
# @File     : base_structure.py
# @Function  :
from functools import reduce
import random

import pandas as pd
import mplfinance as mpf
import json
import talib
import os
import ray


class TradeStructure:
    def __init__(self):
        self.position = self.init_position()
        # self.data = self.load_dataset(data_path)
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
    def init_one_pos_record(asset_name="empty"):
        return {"pos_asset": asset_name,
                "buy_date": "",
                "buy_price": 1,
                "sell_date": "",
                "sell_price": 1,
                "holding_time": 0}

    @staticmethod
    def load_dataset(_data_path, start_stamp="", end_stamp=""):
        df = pd.read_csv(_data_path)
        try:
            df = df[['date', 'open', 'close', 'high', 'low', 'volume', "amount", "turn"]]
            df["market_cap"] = df["amount"] * 100 / df["turn"]
            df["asset_name"] = _data_path.split("/")[-1].replace(".csv", "")

        except Exception as e:
            print(e)
            df = df[['DATES', 'open', 'close', 'high', 'low', 'volume']]
            df = df.rename(columns={"DATES": "date"})
        # print(df)
        df['trade'] = ""
        # df = df[-200:]
        # df.reset_index(drop=True,inplace=True)
        return df

    def base_technical_index(self, ma_parm=(5, 10, 20), macd_parm=(12, 26, 9), kdj_parm=(9, 3)):
        for ma in ma_parm:
            self.data["MA" + str(ma)] = self.data["close"].rolling(ma).mean()
        # 计算MACD指标
        if macd_parm:
            self.data['MACD'], self.data['MACDsignal'], self.data['MACDhist'] = talib.MACD(self.data.close,
                                                                                           fastperiod=macd_parm[0],
                                                                                           slowperiod=macd_parm[1],
                                                                                           signalperiod=macd_parm[2])

        # 计算KDJ指标
        if kdj_parm:
            self.data['slowk'], self.data['slowd'] = talib.STOCH(
                self.data['high'].values,
                self.data['low'].values,
                self.data['close'].values,
                fastk_period=kdj_parm[0],
                slowk_period=kdj_parm[1],
                slowk_matype=0,
                slowd_period=kdj_parm[1],
                slowd_matype=0)
            # 求出J值，J = (3*K)-(2*D)
            self.data['slowj'] = list(map(lambda x, y: 3 * x - 2 * y, self.data['slowk'], self.data['slowd']))

    def cal_technical_index(self):
        pass

    def buy(self, buy_asset="stock", buy_price=1):
        self.position["pos_style"] = buy_asset
        self.position["pos_price"] = buy_price
        self.position['value'] *= (1 - self.trade_rate)

    def sell(self, sell_asset="stock", sell_price=1):
        self.position["pos_style"] = "cash"
        self.position["pos_price"] = 1
        self.position["value"] *= (1 + sell_price / self.position["pre_price"])
        self.position['value'] *= (1 - self.trade_rate)

    def get_buy_sell_signal(self, *args, **kwargs):
        self.data.loc[self.data["long"], "trade"] = "buy"
        self.data.loc[self.data["short"], "trade"] = "sell"

    def strategy_exec(self):
        # self.data.to_csv("result/test_base.csv")
        if len(self.position) == 0:
            return None
        self.pos_tracking = []
        self.position = self.init_position()

        asset_name = self.data.asset_name.unique()[0]
        one_pos_record = self.init_one_pos_record(asset_name=asset_name)
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
                one_pos_record = self.init_one_pos_record(asset_name=asset_name)
            else:
                self.position["pos_style"] = self.position["pre_style"]
                self.position["pos_price"] = row["close"]
                self.position["value"] *= (1 + self.position["pos_price"] / self.position["pre_price"])

    def turn_strategy_exec(self, data):
        self.pos_tracking = []
        one_pos_record = self.init_one_pos_record()

        df_col = data.columns.to_list()

        for index, row in data.iterrows():
            pos_asset = one_pos_record["pos_asset"]
            if pos_asset == "empty":
                buy_pool = []
                for col in df_col:
                    if "_trade" in col and row[col] == "buy":
                        buy_pool.append(col.replace("_trade", ""))
                # print(buy_pool)
                if len(buy_pool) == 0:
                    continue
                buy_asset = random.choice(buy_pool)
                one_pos_record["pos_asset"] = buy_asset
                one_pos_record["buy_date"] = row["date"]
                one_pos_record["buy_price"] = row[buy_asset+"_close"]
                one_pos_record["holding_time"] = -index
            elif row[pos_asset+"_trade"] == "sell":
                one_pos_record["sell_date"] = row["date"]
                one_pos_record["sell_price"] = row[pos_asset+"_close"]
                one_pos_record["holding_time"] += index
                self.pos_tracking.append(one_pos_record.copy())
                one_pos_record = self.init_one_pos_record()

    @staticmethod
    def cal_max_down(df, pct_name="strategy_net", time_stamp="date"):
        res_df = df.copy()
        res_df['max2here'] = res_df[pct_name].expanding().max()
        res_df['dd2here'] = res_df[pct_name] / res_df['max2here'] - 1
        # 计算最大回撤，以及最大回撤结束时间
        end_date, max_draw_down = tuple(res_df.sort_values(by=['dd2here']).iloc[0][[time_stamp, 'dd2here']])
        # 计算最大回撤开始时间
        start_date = res_df[res_df[time_stamp] <= end_date].sort_values(by=pct_name, ascending=False).iloc[0][
            time_stamp]
        # 将无关的变量删除
        res_df.drop(['max2here', 'dd2here'], axis=1, inplace=True)
        return max_draw_down, start_date, end_date

    def eval_index(self, print_log=False):
        eval_df = pd.DataFrame(self.pos_tracking)
        eval_df["pct"] = (eval_df["sell_price"] / (eval_df["buy_price"]*(1+self.trade_rate))) - 1
        eval_df['strategy_net'] = (1 + eval_df['pct']).cumprod()
        eval_df["pct_show"] = eval_df["pct"].apply(lambda x: format(x, '.2%'))

        success_rate = len(eval_df[eval_df["pct"] > 0]) / len(eval_df)
        odds = eval_df["pct"].mean()
        mean_holding_day = eval_df["holding_time"].mean()
        self.data.reset_index(drop=True, inplace=True)
        asset_pct = self.data.close[len(self.data) - 1] / self.data.close[0]
        strategy_pct = eval_df.tail(1)["strategy_net"].item()
        trade_nums = len(eval_df)

        strategy_annual_return = strategy_pct ** (250 / len(self.data)) - 1
        asset_pct_annual_return = asset_pct ** (250 / len(self.data)) - 1

        asset_max_draw_down, asset_start_date, asset_end_date = self.cal_max_down(df=self.data, pct_name="close",
                                                                                  time_stamp="date")
        strategy_max_draw_down, strategy_start_date, strategy_end_date = self.cal_max_down(df=eval_df,
                                                                                           pct_name="strategy_net",
                                                                                           time_stamp="buy_date")

        result_eval = dict()
        result_eval["mean_holding_day"] = mean_holding_day
        result_eval["trade_nums"] = trade_nums

        result_eval["asset_pct"] = asset_pct
        result_eval["strategy_pct"] = strategy_pct

        result_eval["success_rate"] = success_rate
        result_eval["odds"] = odds

        result_eval["strategy_annual_return"] = strategy_annual_return
        result_eval["asset_pct_annual_return"] = asset_pct_annual_return

        result_eval["strategy_max_draw_down"] = strategy_max_draw_down
        result_eval["asset_max_draw_down"] = asset_max_draw_down

        result_eval["strategy_start_date"] = strategy_start_date
        result_eval["strategy_end_date"] = strategy_end_date
        result_eval["asset_start_date"] = asset_start_date
        result_eval["asset_end_date"] = asset_end_date

        if print_log:
            print(eval_df)

            print("平均持股天数:{:.2f}".format(mean_holding_day))
            print("交易次数:{}".format(trade_nums))
            print("标的本身收益率:{:.2f}%".format((asset_pct - 1) * 100))
            print("策略收益率:{:.2f}%".format((strategy_pct - 1) * 100))
            print("策略成功率:{:.2f}%".format(success_rate * 100))
            print("策略赔率:{:.2f}%".format(odds * 100))
            print("策略年化收益率:{:.2f}%".format(strategy_annual_return * 100))
            print("标的年化收益率:{:.2f}%".format(asset_pct_annual_return * 100))

            print("策略最大回撤:{:.2f}%".format(strategy_max_draw_down * 100))
            print("标的最大回撤:{:.2f}%".format(asset_max_draw_down * 100))

            print("策略最大回撤时期:{}==>{}".format(strategy_start_date, strategy_end_date))
            print("标的最大回撤时期:{}==>{}".format(asset_start_date, asset_end_date))

        return result_eval

    def eval_turn_strategy(self, print_log=False):
        eval_df = pd.DataFrame(self.pos_tracking)
        eval_df["pct"] = (eval_df["sell_price"] / eval_df["buy_price"]*(1+self.trade_rate)) - 1
        eval_df['strategy_net'] = (1 + eval_df['pct']).cumprod()
        eval_df["pct_show"] = eval_df["pct"].apply(lambda x: format(x, '.2%'))

        if print_log:
            print(eval_df)

        # return result_eval

    def run_one_stock(self, data_path="", show_buy_and_sell=False, analyze_positions=True,
                      print_log=False, make_plot_param={"is_make_plot": False},
                      bs_signal_param={}, exec_strategy=True):
        self.data = self.load_dataset(data_path)
        self.cal_technical_index()
        self.data.dropna(inplace=True)
        self.get_buy_sell_signal(**bs_signal_param)
        # print(self.data)
        # exit()

        # if len(self.data) < 500 or self.data.market_cap.tail(1).item() < 1e+10:
        #     return None

        if show_buy_and_sell:
            res_list = []
            data_dict = {}
            item_list = ["date", "open", "close", "low", "high", "volume", "trade", "MACD", "MACDsignal", "MACDhist",
                         "slowk", "slowd", "slowj"]
            for index, row in self.data.iterrows():
                for item in item_list:
                    data_dict[item] = row[item]
                res_list.append(data_dict.copy())
            return json.dumps(res_list, indent=2, ensure_ascii=False)
        if not exec_strategy:
            return self.data
        self.strategy_exec()
        if analyze_positions:
            return self.eval_index(print_log=print_log)

        is_make_plot = make_plot_param.get("is_make_plot", False)
        if is_make_plot:
            self.data['Date'] = pd.to_datetime(self.data["date"])
            self.data.set_index('Date', inplace=True)

            my_color = mpf.make_marketcolors(up="red", down="green", edge="inherit", volume="inherit")
            my_style = mpf.make_mpf_style(marketcolors=my_color)
            add_plot = [mpf.make_addplot(self.data[['wma10']])]
            mpf.plot(self.data, type="line", ylabel="price", style=my_style, volume=True, ylabel_lower="volume",
                     addplot=add_plot)

    def run_all_market(self, data_dir="", save_result_path="", limit_list=None, **kwargs):
        # ray.init()
        # data_dir = "/data3/stock_data/stock_data/real_data/bs/post_d/"
        data_list = os.listdir(data_dir)
        result_ = {
            "stock_id": [],
            "mean_holding_day": [],
            "trade_nums": [],
            "asset_pct": [],
            "strategy_pct": [],
            "success_rate": [],
            "odds": [],
            "strategy_annual_return": [],
            "asset_pct_annual_return": [],
            "strategy_max_draw_down": [],
            "asset_max_draw_down": [],
            "strategy_start_date": [],
            "strategy_end_date": [],
            "asset_start_date": [],
            "asset_end_date": [],
        }

        for data_csv in data_list:
            if limit_list is not None:
                if data_csv.replace(".csv", "").replace("sh.", "").replace("sz.", "") not in limit_list:
                    continue
            result_eval = self.run_one_stock(data_path=os.path.join(data_dir, data_csv),
                                             analyze_positions=False, **kwargs)
            if result_eval is not None:
                result_["stock_id"].append(data_csv.replace("csv", ""))

                result_["mean_holding_day"].append(result_eval["mean_holding_day"])
                result_["trade_nums"].append(result_eval["trade_nums"])

                result_["asset_pct"].append(result_eval["asset_pct"])
                result_["strategy_pct"].append(result_eval["strategy_pct"])

                result_["success_rate"].append(result_eval["success_rate"])
                result_["odds"].append(result_eval["odds"])

                result_["strategy_annual_return"].append(result_eval["strategy_annual_return"])
                result_["asset_pct_annual_return"].append(result_eval["asset_pct_annual_return"])

                result_["strategy_max_draw_down"].append(result_eval["strategy_max_draw_down"])
                result_["asset_max_draw_down"].append(result_eval["asset_max_draw_down"])

                result_["strategy_start_date"].append(result_eval["strategy_start_date"])
                result_["strategy_end_date"].append(result_eval["strategy_end_date"])
                result_["asset_start_date"].append(result_eval["asset_start_date"])
                result_["asset_end_date"].append(result_eval["asset_end_date"])

        result = pd.DataFrame(result_)
        result.to_csv(save_result_path, index=False)

    def turn_asset_market(self, data_dir="", save_result_path="", limit_list=None, **kwargs):
        data_list = os.listdir(data_dir)

        df_list = []
        turn_list = []
        for data_csv in data_list:
            if limit_list is not None:
                if data_csv.replace(".csv", "").replace("sh.", "").replace("sz.", "") not in limit_list:
                    continue

            data = self.run_one_stock(data_path=os.path.join(data_dir, data_csv), exec_strategy=False, **kwargs)
            data = data[["date", "close", "trade"]].copy()
            data.rename(columns={'close': data_csv.replace(".csv", "") + '_close',
                                 'trade': data_csv.replace(".csv", "") + '_trade'}, inplace=True)

            turn_list.append(data_csv.replace(".csv", ""))
            df_list.append(data)

        df_merged = reduce(lambda left, right: pd.merge(left, right, on=['date'],
                                                        how='outer'), df_list)

        df_merged.sort_values(by=['date'], inplace=True)
        df_merged = df_merged[-1000:]
        # print(df_merged)
        # df_merged.to_csv("result/tmp.csv", index=False)
        # exit()

        self.turn_strategy_exec(df_merged)
        self.eval_turn_strategy(print_log=True)
