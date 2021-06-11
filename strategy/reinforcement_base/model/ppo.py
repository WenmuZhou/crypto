#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/6/11 15:44
# @Author   : Adolf
# @File     : ppo.py
# @Function  :
import os
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from strategy.reinforcement_base.environment.env_trading import AssetTradingEnv

os.environ["CUDA_VISIBLE_DEVICES"] = "2"
df = pd.read_csv("dataset/stock/stock_handle/600570.csv")

technical_indications_list = ["open", "close", "high", "low", "volume", "ma5", "ma10", "ema12", "ema26", "MACD", "DEA"]
state_shape = 1 + 2 + len(technical_indications_list)

env_kwargs = {
    "state_shape": state_shape,
    "tech_indicator_list": technical_indications_list,
}

env = DummyVecEnv([lambda: AssetTradingEnv(df=df, **env_kwargs)])
PPO_PARAMS = {
    "n_steps": 2048,
    "ent_coef": 0.01,
    "learning_rate": 0.00025,
    "batch_size": 128,
}
model = PPO("MlpPolicy", env, verbose=1, **PPO_PARAMS)

model.learn(total_timesteps=20000)

env_test = DummyVecEnv([lambda: AssetTradingEnv(df=df, **env_kwargs)])
obs = env_test.reset()
for i in range(2000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env_test.step(action)
    env_test.render()
