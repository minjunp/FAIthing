import pandas as pd
from src.indicators import Indicators
import yfinance as yf

"""
Return pd.DataFrame with list of tickers + indicators
"""

class yahooProcessor():
    def __init__(self, tickers, period, intervals, indicators, start = "", end = ""):
        self.tickers = tickers
        self.period = period
        self.intervals = intervals
        self.start = start
        self.end = end
        self.indicators = indicators

    def _get_yfinance_data(self):
        df = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers = self.tickers,

            # Use start/end to set the period
            start = self.start,
            end = self.end,

            # use "period" instead of start/end (leave empty)
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period = self.period,

            # fetch data by interval (including intraday if period < 60 days)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            # (optional, default is '1d')
            interval = self.interval,

            # group by ticker (to access via data['SPY'])
            # (optional, default is 'column')
            group_by = 'ticker',

            # adjust all OHLC automatically
            # (optional, default is False)
            auto_adjust = True,

            # download pre/post regular market hours data
            # (optional, default is False)
            prepost = True,

            # use threads for mass downloading? (True/False/Integer)
            # (optional, default is True)
            threads = True,

            # proxy URL scheme use use when downloading?
            # (optional, default is None)
            proxy = None
        )
        return df

    def _add_indicator(self, df):
        df_combined = pd.DataFrame()

        for ticker in self.tickers:
            df2 = df[ticker]
            df2["tic"] = ticker
            df2 = df2.reset_index(level=0)
            # Add indicators
            if 'RSI' in self.indicators:
                df2 = Indicators.addRSI(df2)
            if 'SMA' in self.indicators:
                df2 = Indicators.addSMA(df2)
            
            # Append to dataframe
            df_combined = pd.concat([df_combined, df2], ignore_index=True)
        
        # drop missing data
        df_combined = df_combined.dropna()
        df_combined = df_combined.reset_index(drop=True)

        # create day of the week column (monday = 0)
        if self.period not in ['1m','2m','5m','15m','30m','60m','90m','1h']:
            df_combined["day"] = df_combined["Date"].dt.dayofweek
            df_combined = df_combined.sort_values(by=["Datetime", "tic"]).reset_index(drop=True)
            
        else:
            df_combined = df_combined.sort_values(by=["Date", "tic"]).reset_index(drop=True)
            # convert date to standard string format, easy to filter
            # df_combined["Date"] = df_combined.Date.apply(lambda x: x.strftime("%Y-%m-%d"))

        print("Shape of DataFrame: ", df.shape)
        
        return df_combined
