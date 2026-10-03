# Intelligent brute force search for solutions to 711 puzzle
# x+y+z+r = 711,
# x*y*z*(711-x-y-z) = 711*10**6 = 79 2^6 3^2 5^6 
# All prices are in cents.
# Let x be the only price divisible by 79; x = k*79, k=1..9;
# actually only k = 1,2,3,4,5,6  allowed, 
# because k=8 cannot satisfy 8*y*z*(79-y-z)=9e6; since 79**3 < 9e6/8,
# and k=7 as a prime factor is excluded by the decomposition of the product. 
# y,z numbers must be in the form 
# y,z = 2^a 3^b 5^c => less than 630 possibilities ea.; 
# a=0..6, b=0..2, c=0..4, so 7*3*5 = 3*35 = 105 possibilities ea. only
# max 6*105^2 ~66k cases to generate, so OK; less (~4.2k) if permutations 
# skipped by checking only y,z,r triplets in ascending order of value.

import numpy as np
yz = np.empty(105,dtype=int)

m = -1
# precompute all possible y or z values
for i in range(7): 
	for j in range(3):
  		for k in range(5):
			m = m + 1
			yz[m] = 2**i * 3**j * 5**k

n = 0
# for all x = k*79
for k in range(1,7):
	x = k*79
	l = 711-x
# check all y <= z <= r pairs 
	for y in yz:
		m = l-y
		for z in yz: 
			r = m-z
			if (y <= z and z <= r):
				n = n+1
				if (k*y*z*r==9000000): print ' prices: ',x,y,z,r,' cents'
print ' checked',n,'  cases' 
