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
import warnings

warnings.filterwarnings('ignore')
from finrl.config import config
from finrl.marketdata.yahoodownloader import YahooDownloader

from finrl.preprocessing.preprocessors import FeatureEngineer
from finrl.preprocessing.data import data_split
from finrl.env.env_stocktrading import StockTradingEnv
from finrl.model.models import DRLAgent
from finrl.trade.backtest import backtest_stats, backtest_plot, get_daily_return, get_baseline

from pprint import pprint

pd.set_option("expand_frame_repr", False)

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
# df = pd.read_csv("dataset/stock/USA/finrl.csv")
# print(df)
# print(df.sort_values(['date', 'tic'], ignore_index=True).head())

# fe = FeatureEngineer(
#     use_technical_indicator=True,
#     tech_indicator_list=config.TECHNICAL_INDICATORS_LIST,
#     use_turbulence=True,
#     user_defined_feature=False)
#
# processed = fe.preprocess_data(df)
# processed.to_csv("dataset/stock/USA/finrl_indicator.csv", index=False)
processed = pd.read_csv("dataset/stock/USA/finrl_indicator.csv")
# print(processed)
list_ticker = processed["tic"].unique().tolist()
# print(list_ticker)
list_date = list(pd.date_range(processed['date'].min(), processed['date'].max()).astype(str))
combination = list(itertools.product(list_date, list_ticker))
processed_full = pd.DataFrame(combination, columns=["date", "tic"]).merge(processed, on=["date", "tic"], how="left")
# print(processed_full)
processed_full = processed_full[processed_full['date'].isin(processed['date'])]
processed_full = processed_full.sort_values(['date', 'tic'])

processed_full = processed_full.fillna(0)
# print(processed_full.sort_values(['date', 'tic'], ignore_index=True).head(10))

train = data_split(processed_full, '2009-01-01', '2019-01-01')
trade = data_split(processed_full, '2019-01-01', '2021-01-01')
# print(len(train))
# print(len(trade))

stock_dimension = len(train.tic.unique())
state_space = 1 + 2 * stock_dimension + len(config.TECHNICAL_INDICATORS_LIST) * stock_dimension
print(f"Stock Dimension: {stock_dimension}, State Space: {state_space}")

env_kwargs = {
    "hmax": 100,
    "initial_amount": 1000000,
    "buy_cost_pct": 0.001,
    "sell_cost_pct": 0.001,
    "state_space": state_space,
    "stock_dim": stock_dimension,
    "tech_indicator_list": config.TECHNICAL_INDICATORS_LIST,
    "action_space": stock_dimension,
    "reward_scaling": 1e-4

}

e_train_gym = StockTradingEnv(df=train, **env_kwargs)

env_train, _ = e_train_gym.get_sb_env()
# print(type(env_train))

agent = DRLAgent(env=env_train)
PPO_PARAMS = {
    "n_steps": 2048,
    "ent_coef": 0.01,
    "learning_rate": 0.00025,
    "batch_size": 128,
}
model_ppo = agent.get_model("ppo", model_kwargs=PPO_PARAMS)

trained_ppo = agent.train_model(model=model_ppo,
                                tb_log_name='ppo',
                                total_timesteps=50000)
