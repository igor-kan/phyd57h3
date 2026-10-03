import numpy as np
import time
import matplotlib.pyplot as plt
plt.interactive(True)

def f(n,x):
    if(n==0):
        return(x*x)
    if(n==1):
        return(x)
    if(n==2):
        return(x*0+1)
    if(n==3):
        return(np.cos(5*x))
    else:
        print('***')
        return(0*x-1)
    
def y(x):
    sum = 0*x
    for n in range(N):
        sum += a[n]*f(n,x)
    return(sum)
    

'''
    fit 4-parametr function to data
    M = # of data points
'''

plt.figure(dpi=140)
N = 4 
M = 100
A = np.zeros((N,N),dtype=float)
a = np.zeros(N)
b = np.zeros(N)
x = np.linspace(0,3,M)
Y = x*(2-x) + 2*(np.random.rand(M) + np.random.rand(M) \
        + np.random.rand(M) +np.random.rand(M) -2) +np.cos(5*x)
plt.scatter(x,Y,s=9,color=(0,0,1),linewidth=1)
plt.grid
plt.show

input(' ok?')

# create A and b
for n in range(N):
    b[n] = np.sum(f(n,x)*Y) # create b_n
    for m in range(N):
        A[m,n] = np.sum(f(n,x)*f(m,x)) # create A_nm
# print('A',A)
# solve Aa = b
a = np.linalg.solve(A,b)
print('a',a)
# create theoretical curve
y_fit = y(x)
a = np.array([-1,2,0,1])
print(' ',a)
y_th = y(x)

plt.ylabel('y, Y')
plt.xlabel('x')
plt.title(' 4-parameter fit to data: y = x*(2-x)+cos(5x)+noise ')
plt.plot(x,y_fit,color=(1,0,0))
plt.plot(x,y_th,color=(0.3,0.3,0.3),alpha=0.7)

input(' ok?')
plt.show

