import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive, cm
from time import time
interactive(True)
'''
   Newton's method
   f' not assumed known analytically, obtained numerically
   0 == f(x0) + f'(x0) (x-x0)    ==>
   x = x0 - f(x0)/f'(x0)
'''
def fun(x):
    return((x-0.43)*(x-0.52)*(x-0.56))

def dfdx(x): 
    return ((fun(x+1e-6) - fun(x-1e-6))/2e-6)


def newton(f,a,b):
    ya = f(a)
    yb = f(b)
    count = 0
    if(ya*yb >0): 
        print(' same signs of function at both limits')
        return((-99.,cout))
    x = (a+b)/2   # zero-th guess
    x_prev = b
    while((count<100) and (abs(x-x_prev)>6e-16)):
        count += 1  
        y = f(x)
        dydx = dfdx(x)
        if (abs(y) < 4e-16):
            return((x,-count))
        if(abs(dydx) == 0.): 
            x += 1e-3
            pass 
        x_prev = x 
        x = x - y/dydx
        print(count,' x',x,' dx',np.around(x-x_prev,12),
                ' y',y)
        plt.scatter(x,y,s=6)
    return((x,count))
        


# main (driver) program
#
t0 = time() 
N = 1000
x = np.linspace(0.25,1.,N)
y = fun(x)
# preview the first and last lines of data
plt.plot(x,y)
plt.grid()
plt.show()

x0,n = newton(fun,0.25,1.)
print(' x0 = ',x0,' count=',n) 
t1 = time() - t0
print('t=',t1)

input(" show detailed plot?")
plt.cla()
x = np.linspace(0.41,0.59,N)
y = fun(x)
plt.plot(x,y)
plt.plot(x,x*0)
plt.scatter(x0,fun(x0))
plt.grid()
plt.title(" Newton's method, x = "+np.str(np.around(x0,8)))
#plt.scatter(xx,yy,s=7)
plt.show()

input(" finish?")

#