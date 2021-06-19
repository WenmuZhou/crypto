#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/31 17:30
# @Author   : Adolf
# @File     : chan_ma.py
# @Function  :
import pandas as pd
from strategy.personalise.loop_pos.strategy_srtucture.base_structure import TradeStructure

pd.set_option("expand_frame_repr", False)
pd.set_option("display.max_rows", 1000)


class ChanMA(TradeStructure):
    def __init__(self, data_path):
        super(ChanMA, self).__init__(data_path)

    def cal_technical_index(self):
        self.data = self.data[:1000]
        self.base_technical_index(ma_parm=(5, 10), kdj_parm=False)

        self.data['diff'] = self.data.apply(lambda x: 10 * (x.MA5 - x.MA10) / min(x.MA5, x.MA10), axis=1)
        self.data["diff_ma"] = self.data["diff"].rolling(9).mean()

        self.data["mom5"] = self.data["close"].pct_change(10)
        self.data["mom10"] = self.data["close"].pct_change(20)

        self.data["mom_ma5"] = self.data.mom5.rolling(5).mean()
        self.data["mom_ma10"] = self.data.mom5.rolling(10).mean()

        # "pearson","kendall","spearman"
        # print(self.data.corr("pearson"))
        # plt.plot(self.data["date"], self.data["MACD"], label="MACD")
        # plt.plot(self.data["date"], self.data["diff_ma"], label="DIFF")
        #
        # plt.legend()
        #
        # plt.show()
        self.data.dropna(inplace=True)
        self.data.reset_index(drop=True, inplace=True)

        print(self.data)


if __name__ == '__main__':
    mawind = ChanMA(data_path="dataset/stock/day/600570_post.csv")
    mawind.cal_technical_index()
    # mawind(analyze_positions=True)
