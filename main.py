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

# Plot it!
stock.plot(x_interval=100)

# Plot between two dates!
stock.plot(x_interval=100, start_date="09/28/14", end_date="11/02/15")

# Plot some elements from the stock!
stock.plot(x_interval=100, columns=["open", "high", "low", "close"])

