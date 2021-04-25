#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/22 14:06
# @Author   : Adolf
# @File     : crypto_env.py
# @Function  :
import numpy as np
import pandas as pd
import random

import gym
from gym import spaces

gym.logger.set_level(40)

# 最终回报步数
MAX_ACCOUNT_BALANCE = 2147483647
# 初始账户余额
INITIAL_ACCOUNT_BALANCE = 100000


class CryptoEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(CryptoEnv, self).__init__()
        self.df = df
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)

        # Actions of the format Buy x%, Sell x%, Hold, etc.
        self.action_space = spaces.Box(
            low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)

        print(self.action_space)
        # Prices contains the OHCL values for the last five prices
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(6, 6), dtype=np.float16)

        print(self.observation_space)

    def step(self, action):
        pass

    def _next_observation(self):
        pass

    def reset(self):
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.max_net_worth = INITIAL_ACCOUNT_BALANCE

        self.shares_held = 0
        self.cost_basis = 0
        self.total_shares_sold = 0
        self.total_sales_value = 0

        self.current_step = random.randint(0, len(self.df.loc[:, 'open'].values) - 6)
        return self._next_observation()

    def render(self, mode='human', close=False):
        pass


if __name__ == '__main__':
    df = pd.read_csv("dataset/1d/BTC.csv")
    crypto_env = CryptoEnv(df)
