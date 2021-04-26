#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/4/22 14:06
# @Author   : Adolf
# @File     : crypto_env_v0.py
# @Function  :
import numpy as np
import pandas as pd
import random

import gym
from gym import spaces

gym.logger.set_level(40)

# 最终回报步数
MAX_ACCOUNT_BALANCE = 2147483647

MAX_NUM_SHARES = 2147483647

# 初始账户余额
INITIAL_ACCOUNT_BALANCE = 100000
MAX_SHARE_PRICE = 5000

MAX_STEPS = 20000


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
        self._take_action(action)

        self.current_step += 1

        if self.current_step > len(self.df.loc[:, 'open'].values) - 6:
            self.current_step = 0

        delay_modifier = (self.current_step / MAX_STEPS)
        reward = self.balance * delay_modifier

        done = self.net_worth <= 0

        obs = self._next_observation()
        return obs, reward, done, {}

    def _take_action(self, action):
        current_price = random.uniform(
            self.df.loc[self.current_step, "open"],
            self.df.loc[self.current_step, "close"])

        action_type = action[0]
        amount = action[1]

        if action_type < 1:
            # Buy amount % of balance in shares
            total_possible = self.balance / current_price
            shares_bought = total_possible * amount
            prev_cost = self.cost_basis * self.shares_held
            additional_cost = shares_bought * current_price
            self.balance -= additional_cost
            self.cost_basis = (prev_cost + additional_cost) / (self.shares_held + shares_bought)
            self.shares_held += shares_bought

        elif action_type < 2:
            # Sell amount % of shares held
            shares_sold = int(self.shares_held * amount)
            self.balance += shares_sold * current_price
            self.shares_held -= shares_sold
            self.total_shares_sold += shares_sold
            self.total_sales_value += shares_sold * current_price

        self.net_worth = self.balance + self.shares_held * current_price

        if self.net_worth > self.max_net_worth:
            self.max_net_worth = self.net_worth
        if self.shares_held == 0:
            self.cost_basis = 0

    def _next_observation(self):
        frame = np.array([
            self.df.loc[self.current_step: self.current_step +
                                           5, 'open'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step +
                                           5, 'high'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step +
                                           5, 'low'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step +
                                           5, 'close'].values / MAX_SHARE_PRICE,
            self.df.loc[self.current_step: self.current_step +
                                           5, 'vol'].values / MAX_NUM_SHARES,
        ])

        obs = np.append(frame, [[
            self.balance / MAX_ACCOUNT_BALANCE,
            self.max_net_worth / MAX_ACCOUNT_BALANCE,
            self.shares_held / MAX_NUM_SHARES,
            self.cost_basis / MAX_SHARE_PRICE,
            self.total_shares_sold / MAX_NUM_SHARES,
            self.total_sales_value / (MAX_NUM_SHARES * MAX_SHARE_PRICE),
        ]], axis=0)
        return obs

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
        profit = self.net_worth - INITIAL_ACCOUNT_BALANCE

        print(f'Step: {self.current_step}')
        print(f'Balance: {self.balance}')
        print(f'Shares held: {self.shares_held}(Total sold: {self.total_shares_sold})')
        print(f'Avg cost for held shares: {self.cost_basis}(Total sales value: {self.total_sales_value})')
        print(f'Net worth: {self.net_worth}(Max net worth: {self.max_net_worth})')
        print(f'Profit: {profit}')


if __name__ == '__main__':
    df = pd.read_csv("dataset/1d/BTC.csv")
    crypto_env = CryptoEnv(df)
