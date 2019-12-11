import pandas as pd
import numpy as np

stockTickers = pd.read_csv("data/available_tickers.csv")

allTickers = np.sort(stockTickers.Ticker)

print("There are %d stocks available: " % len(allTickers))

print(allTickers)