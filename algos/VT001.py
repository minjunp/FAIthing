import sys
sys.path.append('/Users/minjunpark/Documents/RLfinance')

import pandas as pd
import numpy as np
import time
from data_loader import data_loader
from backtesting.backtest import backtest_stats, backtest_plot, get_daily_return, get_baseline
from backtesting.func import calculate_df_account_val
from utils import save_output
"""
    Volatility Algorithm: Buy if -3% for index stock (DOW, SPY), Sell if +3% for index stock (DOW, SPY)
    Inputs:
        tickers: list of tickers to track

    Output:
        pd.DataFrame that stores buy/sell info
""" 

def main():
    # Create relevant directory
    save_output.create_dir()

    tickers = 'SPY'
    period = '10y'
    intervals = '1d'
    indicators = []

    df = data_loader.yahooProcessor(tickers, period, intervals, indicators)._get_yfinance_data()
    closePrice = df.Close
    pct_change = closePrice.pct_change(periods=1).fillna(0) * 100 # Multiply by 100 to change to percent (%)

    actions = (len(pct_change)+1) * [0]
    threshold = 2
    num = 10
    for i, val in enumerate(pct_change):
        # More than threshold drop -- buy
        if val < -threshold:
            actions[i] += num
            actions[i+1] -= num
        # More than threshold rise -- sell
        elif val > threshold:
            actions[i] -= num
            actions[i+1] += num
    
    # Delete last element that was included to prevent index error
    actions = actions[:-1]

    df_actions = pd.DataFrame(closePrice)
    df_actions['Actions'] = actions

    df_account_value = calculate_df_account_val(df_actions, baseline=10000)
    df_account_value = df_account_value.reset_index(level=0)
    df_account_value.rename(columns={'Date': 'date'}, inplace=True)

    # Backtesting
    print("==============Get Backtest Results===========")
    perf_stats_all = backtest_stats(account_value=df_account_value)
    perf_stats_all = pd.DataFrame(perf_stats_all)

    # Baseline stats, change with config time period
    print("==============Get Baseline Stats===========")
    baseline_df = get_baseline(
            ticker="^DJI", 
            start = '2010-01-01',
            end = '2022-01-01')

    stats = backtest_stats(baseline_df, value_col_name = 'close')

    # Backtest plot
    print("==============Compare to DJIA===========")
    # S&P 500: ^GSPC
    # Dow Jones Index: ^DJI
    # NASDAQ 100: ^NDX
    backtest_plot(df_account_value, 
                baseline_ticker = '^DJI', 
                baseline_start = '2010-01-01',
                baseline_end = '2022-01-01')

if __name__ == "__main__":
    start = time.process_time()
    main()
    print(time.process_time() - start)