import sys
sys.path.append('/Users/minjunpark/Documents/RLfinance')

import pandas as pd
import numpy as np
import time
from data_loader import data_loader
from backtesting.backtest import backtest_stats, backtest_plot, get_daily_return, get_baseline

# class VT001:
#     """
#     Volatility Algorithm: Buy if -3% for index stock (DOW, SPY), Sell if +3% for index stock (DOW, SPY)
#     Inputs:
#         tickers: list of tickers to track

#     Output:
#         pd.DataFrame that stores buy/sell info
#     """
#     def __init__(self, tickers):
#         self.tickers = tickers
    
#     def get_yfinance_data(self):
#         df = yf.Ticker(self.tickers).history(period="max")
#         return df



# algo = VT001(['SPY'])
# print(algo.get_yfinance_data())
"""
    Volatility Algorithm: Buy if -3% for index stock (DOW, SPY), Sell if +3% for index stock (DOW, SPY)
    Inputs:
        tickers: list of tickers to track

    Output:
        pd.DataFrame that stores buy/sell info
""" 

def main():
    tickers = 'SPY'
    period = '10y'
    intervals = '1d'
    indicators = []

    df = data_loader.yahooProcessor(tickers, period, intervals, indicators)._get_yfinance_data()
    closePrice = df.Close
    pct_change = closePrice.pct_change(periods=1).fillna(0) * 100 # Multiply by 100 to change to percent (%)

    decisions = (len(pct_change)+1) * [0]
    threshold = 3
    num = 10

    for i, val in enumerate(pct_change):
        # More than threshold drop -- buy
        if val < -threshold:
            decisions[i] += num
            decisions[i+1] -= num
        # More than threshold rise -- sell
        elif val > threshold:
            decisions[i] -= num
            decisions[i+1] += num

    decisions = decisions[:-1]

    # Get df_account_value: Adding total asset in the end after executing an action
    # self.asset_memory.append(end_total_asset)
    # Dummy vec has env_method functionality

    # Backtesting
    print("==============Get Backtest Results===========")
    perf_stats_all = backtest_stats(account_value=df_account_value)
    perf_stats_all = pd.DataFrame(perf_stats_all)

    # Baseline stats, change with config time period
    print("==============Get Baseline Stats===========")
    baseline_df = get_baseline(
            ticker="^DJI", 
            start = config.BACKTEST_START_DATE,
            end = config.BACKTEST_END_DATE)

    stats = backtest_stats(baseline_df, value_col_name = 'close')

    # Backtest plot
    print("==============Compare to DJIA===========")
    # S&P 500: ^GSPC
    # Dow Jones Index: ^DJI
    # NASDAQ 100: ^NDX
    backtest_plot(df_account_value, 
                baseline_ticker = '^DJI', 
                baseline_start = config.BACKTEST_START_DATE,
                baseline_end = config.BACKTEST_END_DATE)

if __name__ == "__main__":
    start = time.process_time()
    main()
    print(time.process_time() - start)