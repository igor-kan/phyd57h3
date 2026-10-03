'''
How to use two pseudorandom distributions
'''
import numpy as np
import matplotlib.pyplot as plt
plt.interactive(True)

N = int(1e6) 

rand = 100 +  120*( np.random.rand(N) -0.5)  # uniform PDF
print(rand)
# plot histogram of uniform rand #s
n = plt.hist(rand,500,facecolor='b',alpha=0.7)
plt.grid(True)
plt.show()

ans = input("next?")

rand = 100 + 15 * np.random.randn(N)      # normal PDF
# plot histogram of normal rand #s
n = plt.hist(rand,500,facecolor='g',alpha=0.7)
plt.grid(True)
plt.show()

# equivalent function:  np.random.normal(size=N)

ans = input("next?")
