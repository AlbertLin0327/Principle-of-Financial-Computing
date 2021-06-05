=== ***Basic Information*** ===
Author: Albert Lin
Student ID: B08902127
School: National Taiwna University
Version: Python3
Library: Numpy Decimal

=== ***Program Description*** ===
This program is to calculate the put price of the European digital option (binary option) and its hedge ratio under the CRR binomial model. 
The payoff function is $1 if the option is in the money at expiration. 
Combinatorics is used to make your program run in linear time. 

=== ***Input format*** ===
Inputs: S (stock price), X (strike price), r (continuously compounded annual interest rate in percentage), s (annual volatility in percentage), T (time to maturity in years), n (number of time steps of the tree). 
Ex: 100 110 3 50 1 2001

=== ***Output format*** ===
Output: (1) put price and (2) hedge ratio. 
Ex: 0.5864 -0.0121

=== ***Reference*** ===
Prof. Lyu: https://www.csie.ntu.edu.tw/~lyuu/finance1/2021/20210317.pdf
Wikipedia: https://en.wikipedia.org/wiki/Binomial_options_pricing_model