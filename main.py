import pandas as pd
import numpy as np
import math

from stock import Stock
from broker import Broker
from exampleBot import ExampleBot
from martingaleBot import MartingaleBot
from testBot import TestBot

at_ = pd.read_csv("data/available_tickers.csv")
allTickers = np.sort(at_.Ticker)

print("There are %d stocks available: " % len(allTickers))

print(allTickers)

selectedTicker = ""

while selectedTicker not in allTickers:
	selectedTicker = input("Please select a ticker: ").upper()

stock = Stock(selectedTicker)

guh_bot = TestBot()
broker = Broker(stock, [ExampleBot(), guh_bot, MartingaleBot()])

broker.simulate()

guh_bot.plot()

#Broker(Stock("AAPL"), [ExampleBot(), TestBot()]).simulate()


# Plot it!
#stock.plot(x_interval=100)

# Plot between two dates!
#stock.plot(x_interval=100, start_date="01/26/13", end_date="03/19/13")

# Plot some elements from the stock!
#stock.plot(x_interval=100, columns=["open", "high", "low", "close"])