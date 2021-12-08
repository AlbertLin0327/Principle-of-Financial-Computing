# import necessary libraries
import numpy as np
from decimal import Decimal

# Class for American type Asian binary option
class PutOption:
    def __init__(self, stock, strike, interest, volatility, time, depth, bucket):
        self.stock_price = Decimal(stock)
        self.strike_price = Decimal(strike)
        self.interest_rate = Decimal(interest / 100)
        self.volatility_rate = Decimal(volatility / 100)
        self.time = Decimal(time)
        self.depth = int(depth)
        self.deltaT = Decimal(self.time / self.depth)
        self.bucket = int(bucket)
        self.Rhat = Decimal(interest / 100 * time / depth)

    # Calculate the max Price of the asset
    def maxPrice(self, n):
        self.maxA = [
            [0 for _ in range(n + 1)] for __ in range(n + 1)
        ]  # Record price at each node

        for i in range(n + 1):
            for j in range(i + 1):
                self.maxA[i][j] = Decimal(
                    1
                    / Decimal(i + 1)
                    * Decimal(
                        self.stock_price
                        * (1 - Decimal(self.up_ratio ** (i - j + 1)))
                        / Decimal(1 - self.up_ratio)
                        + self.stock_price
                        * Decimal(self.up_ratio ** (i - j))
                        * self.down_ratio
                        * Decimal(1 - self.down_ratio ** j)
                        / Decimal(1 - self.down_ratio)
                    )
                )

    # Calculate the min Price of the asset
    def minPrice(self, n):
        self.minA = [
            [0 for _ in range(n + 1)] for __ in range(n + 1)
        ]  # Record price at each node

        for i in range(n + 1):
            for j in range(i + 1):
                self.minA[i][j] = Decimal(
                    1
                    / Decimal(i + 1)
                    * Decimal(
                        self.stock_price
                        * (1 - Decimal(self.down_ratio ** (j + 1)))
                        / (1 - self.down_ratio)
                        + self.stock_price
                        * Decimal(self.down_ratio ** j)
                        * self.up_ratio
                        * (1 - Decimal(self.up_ratio ** (i - j)))
                        / (1 - self.up_ratio)
                    )
                )

    # Calculate the average Price of the asset
    def avgPrice(self, n, k):
        self.avgA = [
            [[0 for _ in range(k + 1)] for __ in range(n + 1)] for ___ in range(n + 1)
        ]  # Record price at each node

        for i in range(n + 1):
            for j in range(i + 1):
                for m in range(k + 1):
                    self.avgA[i][j][m] = Decimal(
                        Decimal(self.minA[i][j] * (k - m) / k)
                        + Decimal(self.maxA[i][j] * m / k)
                    )

    # Initialize the price for the asset
    def CalProfit(self, n, k):
        self.profit = [[0 for _ in range(k + 1)] for __ in range(n + 1)]

        for i in range(n + 1):
            for m in range(k + 1):
                self.profit[i][m] = 1 if (self.strike_price > self.avgA[n][i][m]) else 0

    def put_price(self):

        # Calculate the up and down factors
        self.up_ratio = Decimal(np.exp(self.volatility_rate * np.sqrt(self.deltaT)))
        self.down_ratio = Decimal(1 / self.up_ratio)

        # Calculate the average price for the Asian Option
        self.maxPrice(self.depth)
        self.minPrice(self.depth)

        self.avgPrice(self.depth, self.bucket)

        # Initialize the profit
        self.CalProfit(self.depth, self.bucket)

        # Probability
        self.p = Decimal(np.exp(self.Rhat) - self.down_ratio) / Decimal(
            self.up_ratio - self.down_ratio
        )

        k = self.bucket
        for j in range(self.depth - 1, -1, -1):
            for i in range(j + 1):

                D = [0] * (k + 1)  # Temporary record for profit
                for m in range(k + 1):

                    # average price
                    avg = self.avgA[j][i][m]

                    # average up price
                    Au = Decimal(
                        (j + 1) * avg
                        + self.stock_price
                        * self.up_ratio ** (j + 1 - i)
                        * self.down_ratio ** i
                    ) / (j + 2)

                    # find l to bound up price
                    l = 0
                    if Au < self.avgA[j + 1][i][0]:
                        l = 0
                    elif self.avgA[j + 1][i][k] < Au:
                        l = k
                    else:
                        for c in range(k + 1):
                            if (
                                self.avgA[j + 1][i][c + 1] >= Au
                                and Au >= self.avgA[j + 1][i][c]
                            ):
                                l = c
                                break

                    # find real up price
                    Cu = -1
                    if l == 0 or l == k:
                        Cu = self.profit[i][l]
                    else:
                        x = (Au - self.avgA[j + 1][i][l + 1]) / (
                            self.avgA[j + 1][i][l] - self.avgA[j + 1][i][l + 1]
                        )
                        Cu = (x * self.profit[i][l]) + ((1 - x) * self.profit[i][l + 1])

                    # average down price
                    Ad = Decimal(
                        ((j + 1) * avg)
                        + (
                            self.stock_price
                            * self.up_ratio ** (j - i)
                            * self.down_ratio ** (i + 1)
                        )
                    ) / (j + 2)

                    # find l
                    l = 0
                    if Ad < self.avgA[j + 1][i + 1][0]:
                        l = 0
                    elif self.avgA[j + 1][i + 1][k] < Ad:
                        l = k
                    else:
                        for c in range(k + 1):
                            if (
                                self.avgA[j + 1][i + 1][c + 1] >= Ad
                                and Ad >= self.avgA[j + 1][i + 1][c]
                            ):
                                l = c
                                break

                    # find real down price
                    Cd = -1
                    if l == 0 or l == k:
                        Cd = self.profit[i + 1][l]
                    else:
                        x = (Ad - self.avgA[j + 1][i + 1][l + 1]) / (
                            self.avgA[j + 1][i + 1][l] - self.avgA[j + 1][i + 1][l + 1]
                        )
                        Cd = (x * self.profit[i + 1][l]) + (
                            (1 - x) * self.profit[i + 1][l + 1]
                        )

                    # find the profit price for asia option
                    D[m] = max(
                        (1 if self.strike_price > avg else 0),
                        Decimal((self.p * Cu) + (1 - self.p) * Cd)
                        * Decimal(np.exp(-self.Rhat)),
                    )

                    # find delta for the price
                    self.delta = (Cu - Cd) / (
                        (self.stock_price) * (self.up_ratio - self.down_ratio)
                    )

                # Copy temporary profit to profit list
                for c in range(k + 1):
                    self.profit[i][c] = D[c]

        return round(self.profit[0][0], 4), round(self.delta, 4)


# main function
def main():

    # take in the input from user
    while True:
        try:
            stock, strike, interest_rate, volatility, time, depth, bucket = map(
                float, input().split()
            )
            break

        except:
            print("WRONG FORMAT!!!")

    asian_option = PutOption(
        stock, strike, interest_rate, volatility, time, depth, bucket
    )
    print(*asian_option.put_price())


if __name__ == "__main__":
    main()
