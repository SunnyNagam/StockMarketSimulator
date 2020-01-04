from stock import Stock
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import datetime as dt

class Broker:

	defaultStartingBalance = 1000

	def __init__(self, stock, bots):
		self.stock = stock

		self.accounts = []

		# Open an account for every bot provided
		for bot in bots:
			self.accounts.append({
					"balance": self.defaultStartingBalance,
					"balanceHistory": [],
					"valueHistory": [],
					"bot": bot,
					"currentShares": 0,
					"totalSharesBought": 0,
					"totalSharesSold": 0
				})


	def simulate(self):
		stock = self.stock.data

		for day in range(len(stock["date"])):
			for account in self.accounts:

				# Provide todays info to bot and ask for action in format ("buy"/"sell", #of shares)
				ret = account["bot"].simulateDay(stock["date"][day], stock["open"][day], stock["high"][day], stock["low"][day], stock["close"][day], stock["volume"][day])
				
				# Check if bot's account is able to fulfill order
				orderIsValid = self.checkOrderValidity(account, ret, day)
				
				if orderIsValid and ret[0] is "buy":
					#print("%s placed buy order of %d shares valued at $%d/share on %s" % (account["bot"].name, ret[1], stock["close"][day], stock["date"][day]))
					account["balance"] -= ret[1] * stock["close"][day]
					account["totalSharesBought"] += ret[1]
					account["currentShares"] += ret[1]
				
				elif orderIsValid and ret[0] is "sell":
					#print("%s placed sell order of %d shares valued at $%d/share on %s" % (account["bot"].name, ret[1], stock["close"][day], stock["date"][day]))
					account["balance"] += ret[1] * stock["close"][day]
					account["totalSharesSold"] += ret[1]
					account["currentShares"] -= ret[1]

				# Update balance history
				account["balanceHistory"].append(account["balance"])
				account["valueHistory"].append(account["balance"] + account["currentShares"] * stock["close"][day])

		# Sell all remaining stocks at the end of simulation time limit
		for account in self.accounts:
				account["balance"] += account["currentShares"] * stock["close"][len(stock["date"])-1]
				#account["totalSharesSold"] += account["currentShares"]
				account["currentShares"] = 0
				account["balanceHistory"][-1] = account["balance"]

		# Display info about how bots performed
		for account in self.accounts:
			print("** Bot %s's " % account["bot"].name)
			print("\tStarting balance: %d" % self.defaultStartingBalance)
			print("\tFinal balance: %d" % account["balance"])
			print("\tPercent gain: %f percent" % (((account["balance"]-self.defaultStartingBalance)/self.defaultStartingBalance)*100))
			print("\tBUY AND HOLD GAIN: %f percent" % (((stock["close"][len(stock["date"])-1]-stock["close"][0])/stock["close"][0])*100))
			print("\tTotal shares bought: %d" % account["totalSharesBought"])
			print("\tTotal shares sold: %d" % account["totalSharesSold"])
		
		self.plotBalances()


	def checkOrderValidity(self, account, order, day):
		price = self.stock.data["close"][day]

		if order[0] is "buy":
			if account["balance"] > price * order[1]:
				return True
			return False

		elif order[0] is "sell":
			if account["currentShares"] > order[1]:
				return True
			return False

	def plotBalances(self):
		start = self.defaultStartingBalance
		x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in self.stock.data["date"]]
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y')) #display the date properly

		BAHProfit = (self.stock.data["close"] - self.stock.data["close"][0]) / self.stock.data["close"][0] * 100 +100
		plt.plot(x, BAHProfit, label="Buy and Hold")

		for bot in self.accounts:
			botProfit = ([(b - start)/start*100 + 100 for b in bot["valueHistory"]])
			plt.plot(x, botProfit, label=bot["bot"].name)

		# Configure chart settings
		plt.legend()
		plt.grid(True) #turns on axis grid
		#plt.ylim(0) #sets the y axis min to zero
		plt.xticks(rotation=90, fontsize = 10) #rotates the x axis ticks 90 degress and font size 10
		plt.title("Bots and market performance on %s" % self.stock.ticker) #prints the title on the top
		plt.ylabel('Portfolio (percent)') #labels y axis
		plt.xlabel('Date') #labels x axis
		plt.tight_layout()

		plt.show()
