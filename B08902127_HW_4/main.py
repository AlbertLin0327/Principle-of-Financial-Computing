# import necessary libraries
import math
import numpy as np
from decimal import Decimal


# Class for up-and-out American-style Asian puts option
class AmericanAsianPuts:
	def __init__(self, spot, strike, barrier, time, interest, volatility, period, simulations, degree=2):
		self.spot_price = spot
		self.strike_price = strike
		self.barrier_level = barrier
		self.time = time
		self.interest_rate = interest
		self.volatility_rate = volatility
		self.period = int(period)
		self.path =  int(simulations)
		self.deltaT = time / period
		self.degree = degree


	# Generate random path
	def random_path(self):

		# Randomized the path of Brownian Motions
		self.randomWalk = np.zeros((self.path, self.period + 1))

		# Initialize price
		self.randomWalk[:, 0] = self.spot_price

		# Random Walk each period. The price follow brownian motion
		for i in range(1, self.period + 1):
			self.randomWalk[:,i] = self.randomWalk[:,i - 1] * np.exp((self.interest_rate - (self.volatility_rate ** 2) / 2) * self.deltaT + \
							 self.volatility_rate * np.sqrt(self.deltaT) * np.random.normal(size=self.path))


	# Calculate the mean price and potential payoff 
	def init_maturity(self):

		# Mean price of each path for the beginning to current
		self.meanPrice = np.cumsum(self.randomWalk, axis=1) / (1 + np.arange(self.period + 1))

		# Payoff for each period of each paths
		self.payoff = np.maximum(0, self.strike_price - self.meanPrice)

		# Up and out option
		self.valid = self.meanPrice < self.barrier_level



	# Apply least square method on all path
	def pricing(self):
		
		# Find current best price
		Y = np.where(np.all(self.valid, axis=1), self.payoff[:, -1], 0)

		for i in range(self.period - 2, -1, -1):

			# Calculate discount
			Y *= np.exp(-self.interest_rate * self.deltaT)

			# Find valid path
			hold = self.valid[:, :i + 1].all(axis=1) & (self.payoff[:, i] > 0)

			if np.count_nonzero(self.meanPrice[hold, i]) > 0:

				# Apply Least square method
				regression = np.polyfit(self.meanPrice[hold, i], Y[hold], self.degree)

				CV = np.polyval(regression, self.meanPrice[hold, i])

				# Whether to exercise now
				Y[hold] = np.where(self.payoff[hold, i] > CV, self.payoff[hold, i], Y[hold])
		
		Y *= np.exp(-self.interest_rate * self.deltaT)

		# Calculate put price and standard deviation with best exercise
		self.putPrice = np.sum(Y) / self.path
		self.std = np.std(Y) / np.sqrt(self.path)


def calculate_delta(Model, dS):

	price = Model.putPrice

	# Shift the path
	Model.randomWalk *= (1 + dS)

	Model.init_maturity()
	Model.pricing()

	return (Model.putPrice - price) / (Model.spot_price * dS)

# main function
def main():

	# take in the input from user
	while True:
		try:
			spot, strike, barrier, time, interest, volatility, period, simulations = map(float, input().split())
			break

		except:
			print("WRONG FORMAT!!!")

	monteCarloPut = AmericanAsianPuts(spot, strike, barrier, time, interest, volatility, period, simulations)

	monteCarloPut.random_path()
	monteCarloPut.init_maturity()
	monteCarloPut.pricing()

	# Estimator of delta 
	dS = np.random.uniform(0.001, 0.01)

	delta = calculate_delta(monteCarloPut, dS)

	print(round(monteCarloPut.putPrice, 4), round(monteCarloPut.std, 4), round(delta, 4))


if __name__ == '__main__':
	main()




	

		



