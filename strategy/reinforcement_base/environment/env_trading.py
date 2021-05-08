#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : crypto
# @Time     : 2021/5/3 0:02
# @Author   : Adolf
# @File     : env_trading.py
# @Function  :
import numpy as np
import pandas as pd
import gym
from gym import spaces
from gym.utils import seeding

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

pd.set_option("expand_frame_repr", False)


class EnvTrading(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self,
                 df,
                 asset_dim,
                 hmax,
                 initial_amount,
                 buy_cost_pct,
                 sell_cost_pct,
                 reward_scaling,
                 state_space,
                 action_space,
                 tech_indicator_list,
                 turbulence_threshold=None,
                 make_plots=False,
                 print_verbosity=10,
                 day=0,
                 initial=True,
                 previous_state=[],
                 model_name="",
                 mode="",
                 iteration=""):
        self.df = df
        self.day = day
        self.asset_dim = asset_dim
        self.hmax = hmax
        self.initial_amount = initial_amount
        self.buy_cost_pct = buy_cost_pct
        self.sell_cost_pct = sell_cost_pct
        self.reward_scaling = reward_scaling
        self.state_space = state_space
        self.action_space = action_space
        self.tech_indicator_list = tech_indicator_list

        self.action_space = spaces.Box(low=-1, high=1, shape=(self.action_space,))
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.state_space,))

        self.data = self.df.loc[self.day, :]
        self.terminal = False

        self.make_plots = make_plots
        self.print_verbosity = print_verbosity
        self.turbulence_threshold = turbulence_threshold
        self.initial = initial

        self.previous_state = previous_state
        self.model_name = model_name
        self.mode = mode
        self.iteration = iteration

        self.state = self._initiate_state()

        # initialize reward
        self.reward = 0
        self.turbulence = 0
        self.cost = 0
        self.trades = 0
        self.episode = 0

        # memorize all the total balance change
        self.asset_memory = [self.initial_amount]
        self.rewards_memory = []
        self.actions_memory = []
        self.date_memory = [self._get_date()]

        # self.reset()
        self._seed()

    def step(self, action):
        self.terminal = self.day >= len(self.df.index.unique()) - 1
        if self.terminal:
            if self.make_plots:
                self._make_plot()

    def reset(self):
        self.state = self._initiate_state()

        if self.initial:
            self.asset_memory = [self.initial_amount]
        else:
            previous_total_asset = self.previous_state[0] + \
                                   sum(np.array(self.state[1:(self.asset_dim + 1)]) * np.array(
                                       self.previous_state[(self.asset_dim + 1):(self.asset_dim * 2 + 1)]))
            self.asset_memory = [previous_total_asset]

        self.day = 0
        self.data = self.df.loc[self.day, :]
        self.turbulence = 0
        self.cost = 0
        self.trades = 0
        self.terminal = False
        # self.iteration=self.iteration
        self.rewards_memory = []
        self.actions_memory = []
        self.date_memory = [self._get_date()]

        self.episode += 1

        return self.state

    def render(self, mode='human'):
        return self.state

    def _initiate_state(self):
        if self.initial:
            if len(self.df.code.unique()) > 1:
                state = [self.initial_amount] + \
                        self.data.close.values.tolist() + \
                        [0] * self.asset_dim + \
                        sum([self.data[tech].values.tolist() for tech in self.tech_indicator_list], [])
            else:
                state = [self.initial_amount] + \
                        [self.data.close] + \
                        [0] * self.asset_dim + \
                        sum([[self.data[tech]] for tech in self.tech_indicator_list], [])

        else:
            if len(self.df.code.unique()) > 1:
                # for multiple stock
                state = [self.previous_state[0]] + \
                        self.data.close.values.tolist() + \
                        self.previous_state[(self.asset_dim + 1):(self.asset_dim * 2 + 1)] + \
                        sum([self.data[tech].values.tolist() for tech in self.tech_indicator_list], [])
            else:
                # for single stock
                state = [self.previous_state[0]] + \
                        [self.data.close] + \
                        self.previous_state[(self.asset_dim + 1):(self.asset_dim * 2 + 1)] + \
                        sum([[self.data[tech]] for tech in self.tech_indicator_list], [])
        return state

    def _get_date(self):
        if len(self.df.code.unique()) > 1:
            date = self.data.date.unique()[0]
        else:
            date = self.data.date
        return date

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _make_plot(self):
        plt.plot(self.asset_memory, 'r')
        plt.savefig('results/account_value_trade_{}.png'.format(self.episode))
        plt.close()


if __name__ == '__main__':
    df_btc = pd.read_csv("dataset/1d/BTC.csv")
    df_btc["code"] = "BTC"
    # print(df_btc.code)
    env_trading = EnvTrading(df=df_btc, asset_dim=2)
