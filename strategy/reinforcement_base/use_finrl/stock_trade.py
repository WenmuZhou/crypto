#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/8 13:53
# @Author   : Adolf
# @File     : stock_trade.py
# @Function  :
import os
import pandas as pd
from finrl.preprocessing.data import data_split
from finrl.env.env_stocktrading import StockTradingEnv
from finrl.model.models import DRLAgent
from finrl.trade.backtest import backtest_stats

os.environ["CUDA_VISIBLE_DEVICES"] = "2"
stock_id = "600570"
stock_handle_dir = "dataset/stock/stock_handle/"

df = pd.read_csv(stock_handle_dir + stock_id + ".csv")
df["tic"] = stock_id
# print(df)

train = data_split(df, "2004-02-13", "2018-09-11")
trade = data_split(df, "2018-09-11", "2021-05-25")

technical_indications_list = ["open", "close", "high", "low", "volume", "ma5", "ma10", "ema12", "ema26", "MACD", "DEA"]
stock_dimension = len(train.tic.unique())
state_space = 1 + 2 * stock_dimension + len(technical_indications_list) * stock_dimension

env_kwargs = {
    "hmax": 100,
    "initial_amount": 1000000,
    "buy_cost_pct": 0.001,
    "sell_cost_pct": 0.001,
    "state_space": state_space,
    "stock_dim": stock_dimension,
    "tech_indicator_list": technical_indications_list,
    "action_space": stock_dimension,
    "reward_scaling": 1e-4

}

e_train_gym = StockTradingEnv(df=train, **env_kwargs)
env_train, _ = e_train_gym.get_sb_env()

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
                                total_timesteps=5000)

e_trade_gym = StockTradingEnv(df=trade, **env_kwargs)
df_account_value, df_actions = DRLAgent.DRL_prediction(
    model=trained_ppo,
    environment=e_trade_gym)

perf_stats_all = backtest_stats(account_value=df_account_value)
print(df_actions)
# perf_stats_all = pd.DataFrame(perf_stats_all)
# print(perf_stats_all)
