'''
Simple vector creation; N floats uniformly distr. in [v0,v1)
'''
from time import time
import numpy as np

v0 = 0.1
v1 = 2
N = 1000000     # number of points
k = 100000      # skip this many while printing
c = (v1-v0)/N


print("\nmethod 1: Python loop computes a vector of N floats")
t0 = time()
for i in range(N):
    x = v0 + c*i  
    #if(i//k*k == i):    print(i,x)
t1 = time()-t0; print('t1 = ',np.around(t1,4),'s\n')


print("method 2: np.empty() allocates array, Python fills it")
t0 = time()
# a = np.array(N, dtype = np.float32)
a = np.empty(N)
te = time()-t0
for i in range(N):
    a[i] = v0 + c*i  

#    if(i//k*k == i):    print(i,a[i])
print('t_empty = ' ,np.around(te,6),'s')
t2 = time()-t0; print('t2 = ' ,np.around(t2,4),'s\n')


print("method 3: np.linspace() allocates & fills array")
t0 = time()
b = np.linspace(0.1,2,N,endpoint=False)
#for i in range(N):
#    if(i//k*k == i):    print(i,b[i])  
t3 = time()-t0; print('t3 = ',np.around(t3,4),'s\n')

print("type of a, b: ",type(a),type(b))
print("values of a and b have max |diff| = ",max(abs(a-b)))
print("linspace is ",np.around(t2/t3,2),'x faster than np.empty +loop')
print("linspace is ",np.around(t1/t3,2),'x faster than for loop \n')
