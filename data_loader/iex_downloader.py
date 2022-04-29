# Catalog information
# https://iexcloud.io/core-data-catalog

"""
Interesting features:

Balance Sheet (Last 4 years)
Cash Flow (Last 4 years)
Earnings (Last 4 years)
Income Statement (Last 4 years)
Financials as Reported (Since 2010) --> Not useful since formats differ

Sector Performance (Current time)
Analyst Recommendation (Current time)
"""

import requests
import sys
from config import config
import pandas as pd
import json

class IEXStock:

    def __init__(self, token, symbol, environment='production'):
        if environment == 'production':
            self.BASE_URL = 'https://cloud.iexapis.com/v1'
        else:
            self.BASE_URL = 'https://sandbox.iexapis.com/v1'
        
        self.token = token
        self.symbol = symbol

    def get_logo(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/logo?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_company_info(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/company?token={self.token}"
        r = requests.get(url)

        return r.json()
    
    def get_company_news(self, last=10):
        url = f"{self.BASE_URL}/stock/{self.symbol}/news/last/{last}?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_stats(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/advanced-stats?token={self.token}"
        r = requests.get(url)
        
        return r.json()

    def get_10Q(self, last=2):
        url = f"{self.BASE_URL}/time-series/reported_financials/{self.symbol}/10-Q?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_10K(self, last=2):
        url = f"{self.BASE_URL}/time-series/reported_financials/{self.symbol}/10-K?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()  

    def get_fundamentals(self, period='quarterly', last=4):
        url = f"{self.BASE_URL}/time-series/fundamentals/{self.symbol}/{period}?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()

    """
    last: Specify the number of quarters or years to return. One quarter is returned by default. 
    You can specify up to 12 quarters with quarter, or up to 4 years with annual.
    """
    def get_balance_sheet(self, last=1):
        url = f"{self.BASE_URL}/stock/{self.symbol}/balance-sheet?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_cash_flow(self, last=1):
        url = f"{self.BASE_URL}/stock/{self.symbol}/cash-flow?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_income_statement(self, last=1):
        url = f"{self.BASE_URL}/stock/{self.symbol}/income?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_earnings(self, last=1):
        url = f"{self.BASE_URL}/stock/{self.symbol}/earnings?last={last}&token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_dividends(self, range='5y'):
        url = f"{self.BASE_URL}/stock/{self.symbol}/dividends/{range}?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_institutional_ownership(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/institutional-ownership?token={self.token}"
        r = requests.get(url)

        return r.json()

    def get_insider_transactions(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/insider-transactions?token={self.token}"
        r = requests.get(url)

        return r.json()


def get_sp500_list():
    payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    first_table = payload[0]
    df = first_table

    return df

def save_10Q_data(tickers):
    for ticker in tickers:
        print(ticker)
    p = IEXStock(config.IEX_API_TOKEN, ticker, environment='production')
    tenQ = p.get_10Q(last=9)

    with open(f'../data/10Q/{ticker}_10Q_last9.json', 'w', encoding='utf-8') as f:
        json.dump(tenQ, f, ensure_ascii=False, indent=4)
        
    return None