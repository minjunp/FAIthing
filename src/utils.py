from config import config
import os
import pandas as pd
import yfinance as yf
from indicators import Indicators

def create_dir():
    if not os.path.exists("./" + config.DATA_SAVE_DIR):
        os.makedirs("./" + config.DATA_SAVE_DIR)
    if not os.path.exists("./" + config.TRAINED_MODEL_DIR):
        os.makedirs("./" + config.TRAINED_MODEL_DIR)
    if not os.path.exists("./" + config.TENSORBOARD_LOG_DIR):
        os.makedirs("./" + config.TENSORBOARD_LOG_DIR)
    if not os.path.exists("./" + config.RESULTS_DIR):
        os.makedirs("./" + config.RESULTS_DIR)
    return None

"""
Return pd.DataFrame with list of tickers + indicators
"""
def yahooProcessor(ticker_list, indicator_list, start_date, end_date):
    df = pd.DataFrame()

    # Loop over ticker list
    for tic in ticker_list:
        temp_df = yf.download(tic, start=start_date, end=end_date)
        temp_df["tic"] = tic

        # reset the index, we want to use numbers as index instead of dates
        temp_df = temp_df.reset_index()
        # convert the column names to standardized names
        temp_df.columns = [
            "date",
            "open",
            "high",
            "low",
            "close",
            "adjcp",
            "volume",
            "tic",
        ]
        # use adjusted close price instead of close price
        temp_df["close"] = temp_df["adjcp"]
        # drop the adjusted close price column
        temp_df = temp_df.drop(labels="adjcp", axis=1)
        # Add indicators
        if 'RSI' in indicator_list:
            temp_df = Indicators.addRSI(temp_df)
        if 'SMA' in indicator_list:
            temp_df = Indicators.addSMA(temp_df)

        # Append to dataframe
        df = df.append(temp_df)

    # create day of the week column (monday = 0)
    df["day"] = df["date"].dt.dayofweek
    # convert date to standard string format, easy to filter
    df["date"] = df.date.apply(lambda x: x.strftime("%Y-%m-%d"))
    # drop missing data
    df = df.dropna()
    df = df.reset_index(drop=True)
    print("Shape of DataFrame: ", df.shape)
    # print("Display DataFrame: ", df.head())

    df = df.sort_values(by=["date", "tic"]).reset_index(drop=True)
    return df