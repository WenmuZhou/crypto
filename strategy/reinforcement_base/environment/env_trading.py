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
import matplotlib.pyplot as plt


class AssetTradingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self,
                 df,
                 tech_indicator_list,
                 state_shape,
                 action_shape=1,
                 hmax=100,
                 initial_amount=1000000,
                 reward_scaling=1e-4,
                 buy_cost_pct=0.001,
                 sell_cost_pct=0.001,
                 initial=True,
                 day=0,
                 previous_state=[],
                 make_plots=False,
                 print_verbosity=10, ):
        self.df = df
        self.hmax = hmax
        self.day = day
        self.data = self.df.loc[self.day, :]

        self.initial_amount = initial_amount
        self.buy_cost_pct = buy_cost_pct
        self.sell_cost_pct = sell_cost_pct
        self.tech_indicator_list = tech_indicator_list

        self.previous_state = previous_state
        self.make_plots = make_plots
        # initiate state
        self.terminal = False
        self.initial = initial
        self.state = self._initiate_state()

        # initialize action and state
        self.state_shape = state_shape
        self.action_shape = action_shape

        self.action_space = spaces.Box(low=-1, high=1, shape=(self.action_shape,))
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.state_shape,))

        # initialize reward
        self.reward = 0
        self.cost = 0  # 手续费花费
        self.trades = 0  # 交易次数
        self.episode = 0
        self.reward_scaling = reward_scaling

        # memorize all the total balance change
        self.asset_memory = [self.initial_amount]
        self.rewards_memory = []
        self.actions_memory = []
        self.date_memory = [self.data.date]

        self.print_verbosity = print_verbosity

    def _initiate_state(self):
        if self.initial:
            # For Initial State
            # 账户里初始的余额,当天收盘价,持有股票数为0,各类技术指标的值
            state = [self.initial_amount] + \
                    [self.data.close] + [0] + \
                    sum([[self.data[tech]] for tech in self.tech_indicator_list], [])
        else:
            # Using Previous State
            # 账户里之前的余额,当天收盘价,之前持有的持有股票数,各类技术指标的值
            state = [self.previous_state[0]] + \
                    [self.data.close] + \
                    [self.previous_state[2]] + \
                    sum([[self.data[tech]] for tech in self.tech_indicator_list], [])
        return state

    def _update_state(self):
        state = [self.state[0]] + \
                [self.data.close] + \
                [(self.state[2])] + \
                sum([[self.data[tech]] for tech in self.tech_indicator_list], [])
        return state

    def _sell_asset(self, action):
        if self.state[1] > 0:
            # Sell only if the price is > 0 (no missing data in this particular date)
            # perform sell action based on the sign of the action
            if self.state[2] > 0:
                # Sell only if current asset is > 0
                sell_num_shares = min(abs(action[0]), self.state[2])
                sell_amount = self.state[1] * sell_num_shares * (1 - self.sell_cost_pct)
                # update balance
                self.state[0] += sell_amount

                self.state[2] -= sell_num_shares
                self.cost += self.state[0 + 1] * sell_num_shares * self.sell_cost_pct
                self.trades += 1
            else:
                sell_num_shares = 0
        else:
            sell_num_shares = 0

        return sell_num_shares

    def _buy_asset(self, action):
        if self.state[1] > 0:
            # Buy only if the price is > 0 (no missing data in this particular date)
            available_amount = self.state[0] // self.state[1]
            # print('available_amount:{}'.format(available_amount))

            # update balance
            buy_num_shares = min(available_amount, action[0])
            buy_amount = self.state[1] * buy_num_shares * (1 + self.buy_cost_pct)
            self.state[0] -= buy_amount

            self.state[2] += buy_num_shares
            # self.state[2] = np.add(self.state[2], buy_num_shares, out=self.state[2], casting="unsafe")

            self.cost += self.state[1] * buy_num_shares * self.buy_cost_pct
            self.trades += 1
        else:
            buy_num_shares = 0

        return buy_num_shares

    def step(self, actions):
        self.terminal = self.day >= len(self.df) - 1
        if self.terminal:
            if self.make_plots:
                self._make_plot()
            end_total_asset = self.state[0] + self.state[1] * self.state[2]
            df_total_value = pd.DataFrame(self.asset_memory)

            tot_reward = end_total_asset - self.initial_amount
            df_total_value.columns = ['account_value']

            df_total_value['date'] = self.date_memory
            df_total_value['daily_return'] = df_total_value['account_value'].pct_change(1)
            if df_total_value['daily_return'].std() != 0:
                sharpe = (252 ** 0.5) * df_total_value['daily_return'].mean() / \
                         df_total_value['daily_return'].std()
            df_rewards = pd.DataFrame(self.rewards_memory)
            df_rewards.columns = ['account_rewards']
            df_rewards['date'] = self.date_memory[:-1]

            if self.episode % self.print_verbosity == 0:
                print(f"day: {self.day}, episode: {self.episode}")
                print(f"begin_total_asset: {self.asset_memory[0]:0.2f}")
                print(f"end_total_asset: {end_total_asset:0.2f}")
                print(f"total_reward: {tot_reward:0.2f}")
                print(f"total_cost: {self.cost:0.2f}")
                print(f"total_trades: {self.trades}")
                if df_total_value['daily_return'].std() != 0:
                    print(f"Sharpe: {sharpe:0.3f}")
                print("=================================")

        else:
            actions = actions * self.hmax  # actions initially is scaled between 0 to 1
            actions = (actions.astype(int))  # convert into integer because we can't by fraction of shares

            begin_total_asset = self.state[0] + self.state[1] * self.state[2]

            if actions[0] < 0:
                actions = self._sell_asset(actions) * (-1)
            else:
                actions = self._buy_asset(actions)

            self.actions_memory.append(actions)

            self.day += 1
            self.data = self.df.loc[self.day, :]

            self.state = self._update_state()

            end_total_asset = self.state[0] + self.state[1] * self.state[2]
            self.asset_memory.append(end_total_asset)
            self.date_memory.append(self.data.date)
            self.reward = end_total_asset - begin_total_asset
            self.rewards_memory.append(self.reward)
            self.reward = self.reward * self.reward_scaling

        return self.state, self.reward, self.terminal, {}

    def reset(self):
        # initiate state
        self.state = self._initiate_state()

        if self.initial:
            self.asset_memory = [self.initial_amount]
        else:
            previous_total_asset = self.previous_state[0] + \
                                   [self.state[1] * self.previous_state[2]]
            self.asset_memory = [previous_total_asset]

        self.day = 0
        self.data = self.df.loc[self.day, :]
        self.cost = 0
        self.trades = 0
        self.terminal = False
        self.rewards_memory = []
        self.actions_memory = []
        self.date_memory = [self.data.date]

        self.episode += 1

        return self.state

    def render(self, mode='human'):
        return self.state

    def _make_plot(self):
        plt.plot(self.asset_memory, 'r')
        plt.savefig('results/account_value_trade_{}.png'.format(self.episode))
        plt.close()
