#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/26 13:48
# @Author   : Adolf
# @File     : ppo_base.py
# @Function  :
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from strategy.reinforcement_base.environment.crypto_env_v0 import CryptoEnv

df = pd.read_csv("dataset/1d/BTC.csv")
df_test = pd.read_csv("dataset/1d/ETH.csv")

env = DummyVecEnv([lambda: CryptoEnv(df)])

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=20000)


env_test = DummyVecEnv([lambda: CryptoEnv(df)])
obs = env_test.reset()
for i in range(2000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env_test.step(action)
    env_test.render()
