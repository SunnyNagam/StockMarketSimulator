import numpy as np

def stupid_ema(arr=[], K = 0.2):
	# Sunny's stupid guess for a exponentially weighted moving average
	# function cause he made this thing on a road trip and 
	# doesn't have internet to google how to actually do it

	ans = arr[0]
	for x in range(1, len(arr)):
		ans = K * arr[x] + (1-K) * ans
	return ans


