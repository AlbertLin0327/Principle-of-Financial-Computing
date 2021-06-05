=== ***Basic Information*** ===
Author: Albert Lin
Student ID: B08902127
School: National Taiwna University
Version: Python3
Library: Numpy Decimal

=== ***Program Description*** ===
This program is to calculate the put price of the American-type arithmetic Asian option (binary option) and its delta with Hull-White algorithm.
The payoff function is $1 if the option average in an interval is greater than strike price.
The time complexity of the program is O(N^2 K^2)

=== ***Input format*** ===
Inputs: S (stock price), X (strike price), r (continuously compounded annual interest rate in percentage), s (annual volatility in percentage), T (time to maturity in years), n (number of time steps of the tree), k (number of buckets). 
Ex: 100 95 5 30 1 90 100

=== ***Output format*** ===
Output: (1) put price and (2) delta. 
Ex: 0.3311 -0.0273

=== ***Reference*** ===
Prof. Lyu: https://www.csie.ntu.edu.tw/~lyuu/theses/thesis_d88006.pdf
Financial Engineering and Computation Page 152