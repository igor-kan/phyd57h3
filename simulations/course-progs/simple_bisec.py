import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import interactive, cm
from time import time
interactive(True)
'''
   simple bisection
'''
def fun(x):
    return((x-0.43)*(x-0.52)*(x-0.56))


def bisect(f,a,b):
    ya = f(a)
    yb = f(b)
    count = 0
    if(ya*yb >0 ): 
        print(' same signs of function at both limits')
        return((-99.,cout))
    while(b-a > 1e-15):
        x = (a+b)/2
        yx = f(x)
        count += 1
        if (abs(yx) ==0.):
            return((x,-count))
        if (yx*ya > 0):
            ya = yx
            a = x
        else:
            yb = yx
            b = x
        print(count,'x',x)
        plt.scatter(x,yx,s=10)
    return((x,count))
        


# main (driver) program
#
t0 = time() 
N = 1000
x = np.linspace(0,1.,N)
y = fun(x)
# preview the first and last lines of data
plt.plot(x,y)
plt.grid()
plt.show()

x0,n = bisect(fun,0.,1.)
print(' x0 = ',x0,' count=',n,' y=',fun(x0)) 
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
plt.title("Bisection method"+np.str(np.around(x0,5)))
#plt.scatter(xx,yy,s=7)
plt.show()

input(" finish?")

#