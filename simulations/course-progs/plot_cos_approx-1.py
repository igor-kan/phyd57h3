'''
Approximate cos(x) and plot the approximations
Use exp(x) = sum_{k=0}^inf  (-1)^k x^{2k}/(2k)!
for x = [-2 pi, 2 pi]
'''
import matplotlib.pyplot as plt
import numpy as np
N = 400
x = np.linspace(-np.pi*2,np.pi*2,N) # array of N floats
plt.figure(1, figsize=(9.,6.))
plt.xlabel('X [AU]',fontsize=14)
plt.ylabel('Y [AU]',fontsize=14)
plt.title('cos(x) as Taylor series',fontsize=14)
plt.ylim([-2,3])

# the exact function first
f = np.cos(x)
plt.scatter(x,f,s=6,color=(1.,0,0),linewidth=2) 

y = x*0 + 1   # 0th approximation is exp(x)==1
fact = 1.
Nterms = 40
for k in range(2,Nterms,2):
# update factorial of k  times (-1)^(k/2)
    fact = -fact * (k-1) * k
    # add one term
    y = y + x**k/fact
    # plot the current approx
    plt.plot(x,y)
    if(k<12): plt.text(x[N-1]+.1,y[N-1],str(k))
    print('k',k,' |err|<',max(abs(y-f)))
plt.grid()
plt.show()
