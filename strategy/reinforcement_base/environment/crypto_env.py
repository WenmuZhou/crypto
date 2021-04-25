#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/22 14:06
# @Author   : Adolf
# @File     : crypto_env.py
# @Function  :
import numpy as np
import pandas as pd

import gym
from gym import spaces

MAX_ACCOUNT_BALANCE = 0


class CryptoEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(CryptoEnv, self).__init__()
        self.df = df
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)

        # Actions of the format Buy x%, Sell x%, Hold, etc.
        self.action_space = spaces.Box(
            low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)

        # Prices contains the OHCL values for the last five prices
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(6, 6), dtype=np.float16)

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human', close=False):
        pass


if __name__ == '__main__':
    df = pd.read_csv
    crypto_env = CryptoEnv()