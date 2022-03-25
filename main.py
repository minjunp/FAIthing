
# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
from data_loader import data_loader
import time
from utils.fetch_args import fetch_args
from utils.data_split import data_split

from src.env_stocktrading import StockTradingEnv
from models.models import DRLAgent
from utils import save_output
from trainers.trainer import Trainer
from evaluators.evaluator import Evaluator
from backtesting.backtest import backtest_stats, backtest_plot, get_daily_return, get_baseline
from stable_baselines3 import DDPG

import sys
config = fetch_args()

def main():
    # Create relevant directory
    save_output.create_dir()

    tickers = ['FB', 'AMZN', 'AAPL', 'NVDA', 'GOOG']
    indicators = ['RSI', 'SMA']
    start_date = '2015-01-01'
    end_date = '2016-01-01'

    df = data_loader.yahooProcessor(tickers, indicators, start_date, end_date)

    # Split into train and test
    df_train = data_split(df, '2015-01-01', '2015-06-01')
    df_test = data_split(df, '2015-06-01', '2016-01-01')

    # Get trading environment
    ratio_list = ['RSI_14', 'SMA_25']

    
    # Invoke RL trainer
    mt = Trainer(df_train, ratio_list)
    """
    trained_model, env_kwargs = mt.train_func()
    """

    env_kwargs = mt.get_info()
    trained_model = DDPG.load(f'{config.SAVE_DIR}/{config.currentTime}/{config.TRAINED_MODEL_DIR}/ddpg.zip')

    # Save model
    # Later apply conig name
    save_output.save_model(trained_model, 'ddpg')
    
    # Testing for validation data
    et = Evaluator(df_test, trained_model, env_kwargs)
    df_account_value, df_actions = et.eval_func()

    # Backtesting
    print("==============Get Backtest Results===========")
    perf_stats_all = backtest_stats(account_value=df_account_value)
    perf_stats_all = pd.DataFrame(perf_stats_all)
    save_output.save_to_csv(perf_stats_all, 'perf_stats_all.csv')

    # Baseline stats, change with config time period
    print("==============Get Baseline Stats===========")
    baseline_df = get_baseline(
            ticker="^DJI", 
            start = '2015-06-01',
            end = '2016-01-01')

    stats = backtest_stats(baseline_df, value_col_name = 'close')

    # Backtest plot
    print("==============Compare to DJIA===========")
    # S&P 500: ^GSPC
    # Dow Jones Index: ^DJI
    # NASDAQ 100: ^NDX
    backtest_plot(df_account_value, 
                baseline_ticker = '^DJI', 
                baseline_start = '2015-06-01',
                baseline_end = '2016-01-01')

if __name__ == "__main__":
    start = time.process_time()
    main()
    print(time.process_time() - start)
