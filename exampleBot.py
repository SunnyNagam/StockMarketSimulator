from bot import Bot

class ExampleBot(Bot):

	name = "Example Bot"

	"""
		Super basic example bot, buys on 10 day low, sells on 5 day high.
	"""

	cache = []

	def simulateDay(self, date, open, high, low, close, volume):

		val = (high+low)/2

		self.cache.append(val)

		if len(self.cache) > 10 and val <= min(self.cache[-10:]):
			return ("buy", 1)
		elif len(self.cache) > 5 and val >= max(self.cache[-5:]):
			return ("sell", 1)
		else:
			return ("do nothing")