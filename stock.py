import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class Stock:

	fileTemplate = "data/individual_Stocks_5yr/%s_data.csv"

	def __init__(self, ticker):
		self.ticker = ticker
		self.data = self.loadData()

	def loadData(self):
		return pd.read_csv(self.fileTemplate % self.ticker)

	def printTicker(self):
		print(self.ticker)

	def plot(self, column="high", x_interval=None, y_interval=None):
		x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in self.data["date"]]
		y = self.data[column]

		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y')) #display the date properly

		if x_interval:
			plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=x_interval)) #x axis tick every 60 days
		if y_interval:
			plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(y_interval)) # sets y axis tick spacing to 100

		plt.plot(x,y) #plots the x and y
		plt.grid(True) #turns on axis grid
		plt.ylim(0) #sets the y axis min to zero
		plt.xticks(rotation=90,fontsize = 10) #rotates the x axis ticks 90 degress and font size 10
		plt.title("%s: %s" % (self.ticker, column)) #prints the title on the top
		plt.ylabel('Stock Price For '+ column) #labels y axis
		plt.xlabel('Date') #labels x axis
		plt.tight_layout()

		plt.show()


