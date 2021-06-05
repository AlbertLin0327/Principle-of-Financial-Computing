# import necessary libraries
import numpy as np
from decimal import Decimal


# Class for European Put Option
class PutOption:
	def __init__(self, stock, strike, interest, volatility, time, depth):
		self.stock_price = Decimal(stock)
		self.strike_price = Decimal(strike)
		self.interest_rate = Decimal(interest / 100)
		self.volatility_rate = Decimal(volatility / 100)
		self.time = Decimal(time)
		self.depth = int(depth)
		self.deltaT = Decimal(self.time / self.depth)


	# Calculate the combination for a given N**
	def combination(self, n):
		result = [Decimal(1.0), Decimal(n)]  # default value for first two elements

		# Calculate other elements in O(N) by timing previous * (n - i + 1) / i
		for i in range(2, n + 1):
			result.append(Decimal(result[i - 1]) * Decimal((n - i + 1) / i))

		return result


	def oprion_price_densitivity(self, up_ratio):
		# calculate the price for all the variables in O(N)
		price_distribution = [Decimal(self.stock_price) * Decimal(up_ratio ** self.depth)]

		for i in range(1, self.depth + 1):
			price_distribution.append(price_distribution[i - 1] / Decimal(up_ratio ** 2))

		return price_distribution


	# Calculate the Put price for digital European option
	def put_price(self):

		# Calculate the combination of current tree depth
		factor = self.combination(self.depth - 1)

		# Calculate the up and down factors
		up_ratio = Decimal(np.exp(self.volatility_rate * np.sqrt(self.deltaT)))
		down_ratio = Decimal(1 / up_ratio)

		# Calculate the weighted probability of going up and down TIMES exp(-r * deltaT) for the calculation of Binomial price
		wp_up = (up_ratio - np.exp((-self.interest_rate) * self.deltaT)) / (up_ratio ** 2 - 1)
		wp_down = np.exp((-self.interest_rate) * self.deltaT) - wp_up

		# Calculate the weighted probability dense function in O(N)
		wpdf_up = [Decimal(factor[0]) * (Decimal(wp_up) ** (self.depth - 1))]
		wpdf_down = [Decimal(factor[0]) * (Decimal(wp_up) ** (self.depth - 1))];

		for i in range(1, self.depth):
			wpdf_up.append(Decimal(wpdf_up[i - 1]) * \
				Decimal(wp_down / wp_up) * Decimal(factor[i] / factor[i - 1]))

			wpdf_down.append(Decimal(wpdf_down[i - 1]) * \
				Decimal(wp_down / wp_up) * Decimal(factor[i] / factor[i - 1]))

		# Calculate the possible price of option
		price_distribution = self.oprion_price_densitivity(up_ratio)

		# Sum the up and down option price at depth 1
		uS = Decimal(np.sum([Decimal(wpdf_up[i]) \
			if price_distribution[i] <= self.strike_price else 0 for i in range(self.depth)]))

		dS = Decimal(np.sum([Decimal(wpdf_down[i]) \
			if price_distribution[i + 1] <= self.strike_price else 0 for i in range(self.depth)]))

		# Calculate the binomial put price and hedge ratio
		put_price = Decimal(uS) * Decimal(wp_up) + Decimal(dS) * Decimal(wp_down)
		hedge_ratio = (Decimal(uS) - Decimal(dS)) / Decimal(self.stock_price * (up_ratio - down_ratio))

		print(round(put_price, 4), round(hedge_ratio, 4))



# main function
def main():

	# take in the input from user
	while True:
		try:
			stock, strike, interest_rate, volatility, time, depth = map(float, input().split())
			break

		except:
			print("WRONG FORMAT!!!")

	digital_option = PutOption(stock, strike, interest_rate, volatility, time, depth)
	digital_option.put_price()

if __name__ == '__main__':
	main()
