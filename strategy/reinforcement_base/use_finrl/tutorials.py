#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/4 16:30
# @Author   : Adolf
# @File     : tutorials.py
# @Function  :
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import datetime
import itertools

from finrl.config import config
from finrl.marketdata.yahoodownloader import YahooDownloader

from finrl.preprocessing.preprocessors import FeatureEngineer
from finrl.preprocessing.data import data_split
from finrl.env.env_stocktrading import StockTradingEnv
from finrl.model.models import DRLAgent
from finrl.trade.backtest import backtest_stats, backtest_plot, get_daily_return, get_baseline

from pprint import pprint

if not os.path.exists("result/" + config.DATA_SAVE_DIR):
    os.makedirs("result/" + config.DATA_SAVE_DIR)
if not os.path.exists("result/" + config.TRAINED_MODEL_DIR):
    os.makedirs("result/" + config.TRAINED_MODEL_DIR)
if not os.path.exists("result/" + config.TENSORBOARD_LOG_DIR):
    os.makedirs("result/" + config.TENSORBOARD_LOG_DIR)
if not os.path.exists("result/" + config.RESULTS_DIR):
    os.makedirs("result/" + config.RESULTS_DIR)

# stock_list = ['AAPL', 'MSFT', 'JPM', 'V', 'RTX', 'PG', 'GS', 'NKE', 'DIS', 'AXP', 'HD', 'INTC', 'WMT', 'IBM', 'MRK',
#               'UNH', 'KO', 'CAT', 'TRV', 'JNJ', 'CVX', 'MCD', 'VZ', 'CSCO', 'XOM', 'BA', 'MMM', 'PFE', 'WBA', 'DD']
# stock_list = ["AAPL"]
# df = YahooDownloader(start_date='2009-01-01',
#                      end_date='2021-05-01',
#                      ticker_list=stock_list).fetch_data()

# print(df)
# df.to_csv("dataset/stock/USA/finrl.csv")
df = pd.read_csv("dataset/stock/USA/finrl.csv")
# print(df)
# print(df.sort_values(['date', 'tic'], ignore_index=True).head())

fe = FeatureEngineer(
    use_technical_indicator=True,
    tech_indicator_list=config.TECHNICAL_INDICATORS_LIST,
    use_turbulence=True,
    user_defined_feature=False)

processed = fe.preprocess_data(df)
processed.to_csv("dataset/stock/USA/finrl_indicator.csv")
# processed = pd.read_csv("dataset/stock/USA/finrl_indicator.csv")
# # print(processed)
list_ticker = processed["tic"].unique().tolist()
list_date = list(pd.date_range(processed['date'].min(), processed['date'].max()).astype(str))
combination = list(itertools.product(list_date, list_ticker))

processed_full = pd.DataFrame(combination, columns=["date", "tic"]).merge(processed, on=["date", "tic"], how="left")
processed_full = processed_full[processed_full['date'].isin(processed['date'])]
processed_full = processed_full.sort_values(['date', 'tic'])

processed_full = processed_full.fillna(0)
print(processed_full.sort_values(['date', 'tic'], ignore_index=True).head(10))
