=== ***Basic Information*** ===   
Author: Albert Lin  
Student ID: B08902127  
School: National Taiwna University  
Version: Python3  
Library: math Numpy Decimal  
  
=== ***Program Description*** ===  
This program is to calculate the put price of the up and open american asian put option with least square monte carlo simulations. The Output will fluctuate because of the randomness of the program. The put price will be close to the actual price but delta will fluctuate because of the the randomness. The strategy I use is to give the spot price a shift. The shift is also design to have some randomness in order to provide a a better approximation for different scenarios. Feel free to change the sampling region of dS. 
  
=== ***Input format*** ===  
Inputs: Inputs: S (spot price), X (strike price), H (barrier price), T (years), r (risk-free interest rate), s (volatility), n (number of periods), k (number of simulation paths).    
Ex: 90 100 110 1 0.05 0.30 250 100000  
  
=== ***Output format*** ===  
Output: put price, standard deviation, delta  
Ex: 10.6684 0.0323 -0.6619  
  
=== ***Reference*** ===  
https://www.csie.ntu.edu.tw/~lyuu/finance1/2021/20210512.pdf  

