import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import interactive, cm
from time import time
interactive(True)
'''
   secant method of zero finding
'''
def fun(x):
    return((x-0.43)*(x-0.52)*(x-0.56))


def secant(f,a,b):
    xp = a      # previous point
    yp = f(xp) 
    x  = b      # current point
    y  = f(x)    
    print('start: xp,x,yp,y',xp,x,yp,y)
    count = 0
    while( b-a > 1e-15):
        if (y == yp):
            print(' y=yp: xp,x,yp,y',xp,x,yp,y)
            break
        slope_1 = (x-xp)/(y-yp)
        xp, yp = x, y
        x  = x - y*slope_1  # sort of like Newton
        y  = f(x)
        count += 1
        if (abs(y) == 0.):
            return((x,-count))
        print(count,'x',np.around(x,12),' dx',
                np.around(x-xp,14),
              ' y', y)
        if (count == 100):
            break
        plt.scatter(x,y,s=9)
    return((x,count))
        


# main (driver) program
#
t0 = time() 
N = 1000
x = np.linspace(0,1.,N)
y = fun(x)
plt.plot(x,y)
plt.grid()
x0,n = secant(fun,0.,1.)
plt.title("Secant method")
plt.show()
print(' x0 = ',x0,' count=',n,' y=',fun(x0)) 
t1 = time() - t0
print('t=',t1)
input(" ok?")
plt.cla()
x = np.linspace(0.41,0.59,N)
y = fun(x)
plt.plot(x,y)
plt.plot(x,x*0)
plt.scatter(x0,fun(x0))
plt.grid()
#plt.scatter(xx,yy,s=7)
plt.show()

input(" finish?")

#