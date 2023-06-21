import sys
import os

cwd = os.getcwd()
sys.path.append(f"{cwd}/..")

import pandas as pd
import time
from data_loader import data_loader
from backtesting.backtest import (
    backtest_stats,
    get_baseline,
)
from backtesting.func import calculate_df_account_val
from utils import save_output

import matplotlib.pyplot as plt

def main():
    """
    Fundamental Trading (FT) Algorithm: 
        Buy if below fundamental criteria
        Sell if above fundamental criteria (Use IEX Cloud info)
    Inputs:
        tickers: list of tickers to track

    Output:
        pd.DataFrame that stores buy/sell info
    """
    
    # Create relevant directory
    save_output.create_dir()

    # tickers = ["SPY", "AAPL", "NVDA"]
    tickers = ["SPY"]
    period = "1y"
    interval = "1d"
    indicators = []

    df = data_loader.yahooProcessor(
        tickers, interval, indicators, period=period
    )._get_yfinance_data()

    # for tic in tqdm(tickers):
    #     df_temp = df[tic]
        ## Add Fundamental information to this dataframe -- PE ratio,

    closePrice = df.Close
    pct_change = (
        closePrice.pct_change(periods=1).fillna(0) * 100
    )  # Multiply by 100 to change to percent (%)

    actions = (len(pct_change) + 1) * [0]
    threshold = 2
    num = 10  # Number of stocks to buy / sell
    for i, val in enumerate(pct_change):
        # More than threshold drop -- buy
        if val < -threshold:
            actions[i] += num
            actions[i + 1] -= num
        # More than threshold rise -- sell
        elif val > threshold:
            actions[i] -= num
            actions[i + 1] += num

    # Delete last element that was included to prevent index error
    actions = actions[:-1]

    df_actions = pd.DataFrame(closePrice)
    df_actions["Actions"] = actions

    df_account_value = calculate_df_account_val(df_actions, baseline=10000)
    df_account_value = df_account_value.reset_index(level=0)
    df_account_value.rename(columns={"Date": "date"}, inplace=True)

    df_account_value["date"] = pd.to_datetime(
        df_account_value["date"], format="%Y-%m-%d"
    )

    # Backtesting
    print("==============Get Backtest Results===========")
    perf_stats_all = backtest_stats(account_value=df_account_value)
    perf_stats_all = pd.DataFrame(perf_stats_all)

    # Baseline stats, change with config time period
    print("==============Get Baseline Stats===========")
    baseline_df = get_baseline(
        ticker="^DJI",
        start=str(df_account_value["date"][0])[:10],
        end=str(df_account_value["date"].iloc[-1])[:10],
    )

    # Backtest plot
    # baseline_df
    # df_account_value
    
    df_account_value = df_account_value[:-1]
    baseline_close = baseline_df.close.values
    df_account_value['baseline'] = baseline_close
    
    df_account_value = df_account_value.set_index('date')
    daily_pct_change = df_account_value.pct_change()
    daily_pct_change.fillna(0, inplace=True)
    cumprod_daily_pct_change = (1 + daily_pct_change).cumprod()
    
    def plot_backtest(cum_change):
        fig = plt.figure(figsize=(15, 7))
        ax1 = fig.add_subplot(1, 1, 1)
        cum_change.plot(ax=ax1)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Cumulative return')
        ax1.set_title('Stock Cumulative Returns')
        plt.savefig('pct.png')
        
    plot_backtest(cumprod_daily_pct_change)

    # S&P 500: ^GSPC
    # Dow Jones Index: ^DJI
    # NASDAQ 100: ^NDX

if __name__ == "__main__":
    start = time.process_time()
    main()
    print(time.process_time() - start)
