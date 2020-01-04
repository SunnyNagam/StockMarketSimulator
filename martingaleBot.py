from bot import Bot

class MartingaleBot(Bot):

	name = "Martingale Bot"

	"""
		Bot that trades based on martingale system,
		a known degenerate gambling strat thats almost always a bad idea
	"""

	cache = []
	prev = 1
	sumShares = 0
	dayCount = 0 

	def simulateDay(self, date, open, high, low, close, volume):

		val = close
		self.dayCount += 1

		self.cache.append(val)

		result = ("default", 0)

		if self.dayCount % 3 == 0:
			if val < self.cache[-3] * 0.985:
				self.sumShares += self.prev
				result = ("buy", self.prev)
				#print("** i'm buying %d shares"%self.prev)
				self.prev *= 2
			elif val > self.cache[-3] * 1.015:
				result = ("sell", self.sumShares)
				self.sumShares = 0
				self.prev = 1

		return result