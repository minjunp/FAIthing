import sys
sys.path.append('/Users/minjunpark/Documents/RLfinance')
from config import config
import pandas as pd
import json
import numpy as np
import yfinance as yf

from iex_downloader import IEXStock

config.IEX_API_TOKEN

# There are 2 tables on the Wikipedia page
# we want the first table

payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
first_table = payload[0]
second_table = payload[1]

df = first_table

caps = []
tickers = df.Symbol.tolist()
for ticker in tickers:
    print(ticker)
    try:
        cap = yf.Ticker(ticker).info['marketCap']
        caps.append(int(cap))
    except:
        caps.append(0)


np.savetxt('caps.txt', caps)