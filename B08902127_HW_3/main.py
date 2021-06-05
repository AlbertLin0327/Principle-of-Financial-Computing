# import necessary libraries
import math
import numpy as np
from decimal import Decimal


# Class for European Down in or out Barrier option
class DownBarrierOption:
	def __init__(self, stock, strike, barrier, interest, volatility, time, depth):
		self.stock_price = Decimal(stock)
		self.strike_price = Decimal(strike)
		self.barrier_level = Decimal(barrier)
		self.interest_rate = Decimal(interest / 100)
		self.volatility_rate = Decimal(volatility / 100)
		self.time = Decimal(time)
		self.depth = int(depth)
		self.deltaT = Decimal(self.time / self.depth)

	# Calculate the Put price for digital European option
	def set_essentials(self):

		# Calculate H and lambda
		self.h = math.floor(Decimal(np.log(float(self.stock_price / self.barrier_level))) / (self.volatility_rate * np.sqrt(self.deltaT)))
		self.lmbda = Decimal(np.log(float(self.stock_price / self.barrier_level))) / (self.h * self.volatility_rate * np.sqrt(self.deltaT))

		# Calculate the up and down factors
		self.u = Decimal(np.exp(self.volatility_rate * self.lmbda * np.sqrt(self.deltaT)))
		self.d = Decimal(1 / self.u)

		# Possibility of each move
		self.p_u = Decimal(1 / (2 * self.lmbda ** 2)) + \
				   Decimal((self.interest_rate - self.volatility_rate ** 2 / 2) * np.sqrt(self.deltaT) / (2 * self.lmbda * self.volatility_rate))

		self.p_d = Decimal(1 / (2 * self.lmbda ** 2)) - \
				   Decimal((self.interest_rate - self.volatility_rate ** 2 / 2) * np.sqrt(self.deltaT) / (2 * self.lmbda * self.volatility_rate))

		self.p_m = 1 - self.p_u - self.p_d

	# Initialize the price at strike day
	def init_stock_price(self):

		# calculate the power
		power = [Decimal(1) for i in range(2 * self.depth + 1)]

		for i in range(self.depth):
			power[self.depth + i + 1] = power[self.depth + i] * self.d
			power[self.depth - i - 1] = power[self.depth - i] * self.u

		# build a share price tree of regular option and knock out option
		self.knockout_option_price = [Decimal(0) for i in range(2 * self.depth + 1)]
		self.option_price = [Decimal(0) for i in range(2 * self.depth + 1)]

		# Calculate the final price
		for i in range(2 * self.depth + 1):
			self.option_price[i] = max(0, Decimal(self.strike_price - self.stock_price * power[i]))
			self.knockout_option_price[i] = max(0, Decimal(self.strike_price - self.stock_price * power[i]))

		# The first hit price
		self.knockout_option_price[self.depth + self.h] = Decimal(0)

	# Back traversal the tree
	def back_traversal(self):

		# Calculate the option price at each node
		for i in range(self.depth - 1, -1, -1):
			for j in range(2 * i + 1):

				# Calculate regular option price
				self.option_price[j] = self.p_u * self.option_price[j] + \
									   self.p_m * self.option_price[j + 1] + \
									   self.p_d * self.option_price[j + 2]

				# Calculate knock out option price
				self.knockout_option_price[j] = self.p_u * self.knockout_option_price[j] + \
												self.p_m * self.knockout_option_price[j + 1] + \
												self.p_d * self.knockout_option_price[j + 2]
			
			# Set to 0 if it is a hit
			if i >= self.h:
				self.knockout_option_price[i + self.h] = Decimal(0)


	def pricing(self):
		# setup essential variable 
		self.set_essentials()

		# initialize option price tree
		self.init_stock_price()

		# Calculate option price with back traversal
		self.back_traversal()

		# Calculate option price, knock out price and knock in price
		self.knockout_price = self.knockout_option_price[0] / Decimal(np.exp(self.interest_rate * self.time))

		self.regular_option_price = self.option_price[0] / Decimal(np.exp(self.interest_rate * self.time))

		self.knockin_price = self.regular_option_price - self.knockout_price


# main function
def main():

	# take in the input from user
	while True:
		try:
			stock, strike, barrier, interest_rate, volatility, time, depth = map(float, input().split())
			break

		except:
			print("WRONG FORMAT!!!")

	barrier_option = DownBarrierOption(stock, strike, barrier, interest_rate, volatility, time, depth)
	barrier_option.pricing()

	print(round(barrier_option.knockin_price, 4))


if __name__ == '__main__':
	main()




	

		



