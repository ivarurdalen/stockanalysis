import datetime as dt
import yfinance as yf
import pandas as pd
import numpy as np
import sqlite3

# List of OSE tickers

tickers = pd.read_csv(
    "pages/data/tickers/oslo_tickers.csv", header=None, names=["Ticker"]
)

con = sqlite3.connect("pages/data/stockanalysis.db")
# Download prices from Yahoo Finance

for ticker in tickers["Ticker"]:
    interval = "1d"
    start = dt.datetime(2018, 1, 1)
    end = dt.datetime.today()

    # Download from Yahoo Finance
    prices = yf.download(ticker, start, end, interval=interval)

    # Add ticker column first
    prices["ticker"] = ticker
    cols = prices.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    prices = prices[cols]

    # prices.to_sql("prices", con, if_exists="replace")
    prices.to_sql("prices", con, if_exists="append")
    print(f"Ticker: {ticker}")
