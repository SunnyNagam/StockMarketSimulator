import pandas as pd
import numpy as np

from stock import Stock

stockTickers = pd.read_csv("data/available_tickers.csv")

allTickers = np.sort(stockTickers.Ticker)

print("There are %d stocks available: " % len(allTickers))

print(allTickers)

selectedTicker = ""

while selectedTicker not in allTickers:
	selectedTicker = input("Please select a ticker: ")

stock = Stock(selectedTicker)

stock.plot(x_interval=100)

