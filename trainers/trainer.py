# Import libraries
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('Agg')
import datetime
from pprint import pprint
import sys
import itertools
from data_loader import data_loader

from utils.dirs import create_dir
from utils.fetch_args import fetch_args
from utils.data_split import data_split

from src.env_stocktrading import StockTradingEnv
from models.models import DRLAgent
from utils import save_output
from utils.fetch_args import fetch_args
config = fetch_args()

class Trainer:
    def __init__(self, df_train, ratio_list):
        self.df_train = df_train
        self.ratio_list = ratio_list

    def get_info(self):
        # Get trading environment
        stock_dimension = len(self.df_train.tic.unique())
        state_space = 1 + 2*stock_dimension + len(self.ratio_list)*stock_dimension
        print(f"Stock Dimension: {stock_dimension}, State Space: {state_space}")

        # Parameters for the environment
        env_kwargs = {
            "hmax": 100,
            "initial_amount": 1000000,
            "buy_cost_pct": 0.001,
            "sell_cost_pct": 0.001,
            "state_space": state_space,
            "stock_dim": stock_dimension,
            "tech_indicator_list": self.ratio_list,
            "action_space": stock_dimension,
            "reward_scaling": 1e-4
        }
        return env_kwargs
    
    def train_func(self):
        # Get trading environment info
        env_kwargs = self.get_info()
        # Parameters for the environment

        # Establish the training environment using StockTradingEnv() class
        e_train_gym = StockTradingEnv(df=self.df_train, **env_kwargs)

        # Environment for trading
        env_train, _ = e_train_gym.get_sb_env()
        print(type(env_train))

        # Implement RL algorithms (DDPG: Deep Deterministic Policy Gradient)
        agent = DRLAgent(env = env_train)
        model = agent.get_model("ddpg")
        trained_model = agent.train_model(model=model, 
                                    tb_log_name='ddpg',
                                    total_timesteps=50000)
        
        return trained_model