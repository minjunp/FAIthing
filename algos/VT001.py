import sys

sys.path.append("/Users/minjunpark/Documents/FAIthing")
import pandas as pd
import numpy as np
import time
from data_loader import data_loader
from backtesting.backtest import (
    backtest_stats,
    backtest_plot,
    get_daily_return,
    get_baseline,
)
from backtesting.func import calculate_df_account_val
from utils import save_output

"""
    Volatility Trading (VT) Algorithm: Buy if -3% for index stock (DOW, SPY), Sell if +3% for index stock (DOW, SPY)
    Inputs:
        tickers: list of tickers to track

    Output:
        pd.DataFrame that stores buy/sell info
"""


def main():
    # Create relevant directory
    save_output.create_dir()

    tickers = "SPY"
    period = "10y"
    intervals = "1d"
    indicators = []

    df = data_loader.yahooProcessor(
        tickers, period, intervals, indicators
    )._get_yfinance_data()

    closePrice = df.Close
    pct_change = (
        closePrice.pct_change(periods=1).fillna(0) * 100
    )  # Multiply by 100 to change to percent (%

    # Config & Initialization
    actions = (len(pct_change) + 1) * [0]
    threshold = 2  # N-percent change
    num_own = 0  # number of stocks owned
    fund = 10000  # Initial fund to start with --> Amount at hand
    account_vals = []

    for i, val in enumerate(pct_change):
        maxNum = int(fund / closePrice[i])  # Max number of stocks to trade

        # More than threshold drop --> buy
        if val < -threshold:
            # Update actions
            actions[i] += maxNum
            actions[i + 1] -= maxNum

        # More than threshold rise --> sell
        elif val > threshold:
            # Update actions
            actions[i] -= maxNum
            actions[i + 1] += maxNum

        # Move opposite direction (Sell --> Add to fund, Buy --> Subtract to fund)
        fund -= actions[i] * closePrice[i]
        num_own += actions[
            i
        ]  # Total number of particular stocks owned --> Changed by actions taken

        total_asset = fund + (num_own * closePrice[i])
        account_vals.append(total_asset)

    # Delete last element that was included to prevent index error
    actions = actions[:-1]

    df_actions = pd.DataFrame(closePrice)
    df_actions["Actions"] = actions

    df_account_value = pd.DataFrame(
        {"account_value": account_vals}, index=df_actions.index
    )
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

    stats = backtest_stats(baseline_df, value_col_name="close")

    # Backtest plot
    print("==============Compare to DJIA===========")
    # S&P 500: ^GSPC
    # Dow Jones Index: ^DJI
    # NASDAQ 100: ^NDX
    backtest_plot(
        df_account_value,
        baseline_ticker="^DJI",
        baseline_start=str(df_account_value["date"][0])[:10],
        baseline_end=str(df_account_value["date"].iloc[-1])[:10],
    )


if __name__ == "__main__":
    start = time.process_time()
    main()
    print(time.process_time() - start)
