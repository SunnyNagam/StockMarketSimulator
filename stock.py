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

	def plot(self, columns=["high"],
			x_interval=None, y_interval=None,
			start_date=None, end_date=None):
		x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in self.data["date"]]

		if start_date and end_date:
			startInd, endInd = dateRangeToInds(start_date, end_date, x)
		else:
			startInd, endInd = (0, len(x))

		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y')) #display the date properly

		if x_interval:
			plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=x_interval)) #x axis tick every 60 days
		if y_interval:
			plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(y_interval)) # sets y axis tick spacing to 100

		for field in columns:
			plt.plot(x[startInd:endInd], self.data[field][startInd:endInd], label=field) #plots the x and y

		plt.legend()
		plt.grid(True) #turns on axis grid
		plt.ylim(0) #sets the y axis min to zero
		plt.xticks(rotation=90, fontsize = 10) #rotates the x axis ticks 90 degress and font size 10
		plt.title("%s:" % (self.ticker)) #prints the title on the top
		plt.ylabel('Stock Price') #labels y axis
		plt.xlabel('Date') #labels x axis
		plt.tight_layout()

		plt.show()

def dateRangeToInds(start, end, x=[]):
	"""
		Returns the index of start and end dates in given sorted date array
		On error or invalid params, returns first and last index

		Help from: https://stackoverflow.com/questions/32237862/find-the-closest-date-to-a-given-date
	"""
	start = dt.datetime.strptime(start,'%m/%d/%y').date()
	end = dt.datetime.strptime(end,'%m/%d/%y').date()

	if start < x[0] or start > x[-1] or end < x[0] or end > x[-1]:
		return (0, len(x))

	return (x.index(min(x, key=lambda y: abs(y - start))),
			x.index(min(x, key=lambda y: abs(y - end))))