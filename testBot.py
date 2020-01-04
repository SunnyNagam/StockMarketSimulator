from bot import Bot
from util import stupid_ema
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

class TestBot(Bot):

	name = "GUH-atron 5000"

	"""
		There's a GUH in all of us
		Idea #1: Once value sinks below ema (exponential weighted
		moving average), look for inflection points in distance
		from value to ema 
	"""

	cache = []
	date_cache = []
	ema_cache = []
	ema_dist = []

	debugging_graph = []

	value_sunk = False
	value_swap_inx = 0
	max_dist = 0
	order_handled = False

	def simulateDay(self, date, open, high, low, close, volume):

		val = (high+low)/2
		self.cache.append(val)
		self.date_cache.append(date)
		self.debugging_graph.append(val)

		if len(self.cache) <= 20:
			self.ema_cache.append(0)
			self.ema_dist.append(0)
			return ("do nothin", 0)

		ema = stupid_ema(self.cache[-20:])

		self.ema_cache.append(ema)
		dist = val - ema
		self.ema_dist.append(dist+100)

		if not self.value_sunk and dist < 0:
			self.value_sunk = True
			self.value_swap_inx = len(self.ema_cache) - 1
			self.max_dist = dist
			self.order_handled = False
		if self.value_sunk and dist >= 0:
			self.value_sunk = False
			self.value_swap_inx = len(self.ema_cache) - 1
			self.max_dist = dist
			self.order_handled = False

		if self.value_sunk and not self.order_handled:
			if dist > self.max_dist:
				self.order_handled = True
				self.debugging_graph[-1] *= 0.8
				return ("buy", 1)
			else:
				self.max_dist = dist

		if not self.value_sunk and not self.order_handled:
			if dist < self.max_dist:
				self.order_handled = True
				self.debugging_graph[-1] *= 1.2
				return ("sell", 1)
			else:
				self.max_dist = dist

		return ("nothin", 0)

		# if len(self.cache) > 5 and val <= min(self.cache[-5:]):
		# 	return ("buy", 2)
		# elif len(self.cache) > 10 and val >= max(self.cache[-10:]):
		# 	return ("sell", 1)
		# else:
		# 	return ("do nothing")

	def plot(self):
		x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in self.date_cache]
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y')) #display the date properly

		plt.plot(x, self.cache, label="Value")
		plt.plot(x, self.ema_cache, label="EMA")
		plt.plot(x, self.ema_dist, label="EMA DIST")
		plt.plot(x, self.debugging_graph, label="debug")

		# Configure chart settings
		plt.legend()
		plt.grid(True) #turns on axis grid
		#plt.ylim(0) #sets the y axis min to zero
		plt.xticks(rotation=90, fontsize = 10) #rotates the x axis ticks 90 degress and font size 10
		plt.title("%s's debugging" % self.name) #prints the title on the top
		plt.ylabel('Price') #labels y axis
		plt.xlabel('Date') #labels x axis
		plt.tight_layout()

		plt.show()