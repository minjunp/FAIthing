import pandas as pd
import talib

class Indicators:
    def addRSI(df, timeperiod=14):
        """
        Add RSI based on timeperiod value
        """
        df[f'RSI_{timeperiod}'] = talib.RSI(df.close, timeperiod=timeperiod)

        return df

    def addSMA(df, timeperiod=25):
        """
        Add SMA based on timeperiod value
        """
        df[f'SMA_{timeperiod}'] = talib.SMA(df.close, timeperiod=timeperiod)

        return df