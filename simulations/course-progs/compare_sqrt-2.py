import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive, cm
from time import time
interactive(True)

c = 4  # find sqrt of this number by iteration
xL, xR = 1.75,2.5 
#c = 2
#xL, xR = 1., 2.
plt.figure(dpi=140)

def fun(x):
    return(x*x -c)

def dfdx(x,d): 
    if (d > 0.):
        return ((fun(x+d)-fun(x-d))/(2*d))
    else:
        return (2*x)

def bisect(f,a,b):
    ya = f(a)
    yb = f(b)
    count = 0
    if(ya*yb >0 ): 
        print(' same signs of function at both limits')
        return((-99.,cout))
    while(b-a > 1e-5):
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
        if(x*x == c):
            logerr = -16.5
        else: 
            logerr = np.log10(abs(x-c**0.5))
        plt.scatter(count,logerr,s=13,color=(0,.3,1))
    return((x,count))

'''
   Secant method of sqrt(x) finding. Method with 
   analytical f' and safe division.
'''

def safe_secant(a,b):
    xp = a      # previous point
    x  = b      # current point   
    count = 0
    while(x*x != c):
        # division-free secant method
        #  for function f(x)=1/x-c
        rhs = x - (x*x-c)/(x+xp) 
        xp = x      # update xp
        x  = rhs    # update x 
        count += 1
        print(count,'x',x,' dx',x-xp)
        if(x*x == c):
            logerr = -16.5
        else: 
            logerr = np.log10(abs(x-c**0.5))
        plt.scatter(count,logerr,s=24,color=(.5,.7,.2))
        if(count>10 or abs(x-xp)<1e-16): 
            break
    return((x,count))
        

'''
   Newton's method for 1/x finding
   f' known analytically, or obtained numerically
   0 == f(x0) + f'(x0) (x-x0)    ==>
   x = x0 - f(x0)/f'(x0)
'''

def newton(f,a,b):
    ya = f(a)
    yb = f(b)
    count = 0
    if(ya*yb >0): 
        print('same signs of function at both limits')
        return((-99.,cout))
    x = (a+b)/2   # zero-th guess
    x_prev = b
    while(count<50):
        count += 1
        y = f(x)
        # a guess about the best delta
        delta = 1e-5 *(abs(x-x_prev)/4e-6)**0.25
        dydx = dfdx(x,delta)
        if (abs(y) < 1e-16):
            return((x,-count))
        if(dydx == 0.): 
            x += 1e-4
            pass 
        x_prev = x 
        x = x - y/dydx
        print('%d x %13.9f dx %7.4e y %14.10e  d%14.10e' 
                %(count,x,x-x_prev,y,delta))
        if(x*x == c):
            logerr = -16.5
        else: 
            logerr = np.log10(abs(x-c**0.5))
        plt.scatter(count,logerr,s=22,color=(1,0,0))
        if(abs(x-x_prev)<3e-16):
            break
    return((x,count))
        
'''
  Netwon's method with analytical f/f'
'''
def Newton_sqrt(a,b):
    xp = a      # previous point
    x  = b      # current point   
    count = 0
    while(x != xp):
        # division-free Newton, analytical f'
        # function f(x)=x*x-c => -f/f' = (x-c/x)/2
        xp = x
        x  = x/2 + c/2/x      # x - (x-c/x)/2 
        count += 1
        print(count,'x',x,' dx',x-xp,' err',x-c**0.5)
        if(x-c**0.5==0.):
            logerr = -16.5
        else: 
            logerr = np.log10(abs(x-c**0.5))
        plt.scatter(count,logerr,s=10,color=(0,0,0))
        if (count >50): 
            break
    return((x,count))
        

#-----------------------------------------------------------
# main (driver) program
# find sqrt(3)


# test bisection
x0,n = bisect(fun,xL,xR)
plt.title("Convergence of iterated sqrt("+str(c)+")")
plt.xlabel('iteration number')
plt.grid()
plt.show()

input('bisected. go on? ')

# test secant
t0 = time() 
x0,n = safe_secant(xL,xR)
plt.show()
print('c',c,' x0,err',x0,x0-c**0.5,' count=',n) 
t1 = time() - t0
print('t=',t1)
input(" ok?")
#


#  Newton's method, any function
#
x0,n = newton(fun,xL,xR)
print(' x0 = ',x0,' count=',n) 
#plt.title(" Newton's method, x = "+np.str(np.around(x0,8)))
plt.text(10.1,-8.9, 'blue = bisection')
plt.text(10.1,-10.9,'green = secant')
plt.text(10.1,-12.9,"red = Newton, f' num.")
plt.text(10.1,-14.9,"black = Newton, f' anal.")
plt.ylabel('log$_{10}$ |x - $\sqrt{c}$|')
plt.show()
input(" newton finished. go on? ")


#   Newton's inverse     
x0, count = Newton_sqrt(xL,xR) 
plt.show()
input(" Newton (f' analyt.) finished. go on? ")




# variable order polynomial fitting method
# 

# Lagrange interpolating polynomial
# N points given as x_j,y_j, j=0..N-1.
# P(x) = Sigma_j=0^N-1 f(x_j) Prod_{k!=j} (x-x_k)/(x_j-x_k)
# input: x_n, y_n arrays of length N
# all x's must be different
# output: value p(xx) 
def Lagrange_poly(N,xx):
    p = xx*0
    for j in range(N):
        val = y[j]
        for k in range(N):
            if(j!=k):
                val *= (xx-x[k])/(x[j]-x[k])
    p += val
    return(p)

# derivative of Lagrange interpolating polynomial
# P'(x) = Sum_j=0^N f(x_j) Prod_{k!=j} \
#    Sum_{k} (x-x_k)/(x_j-x_k)
# input: x_n, y_n arrays of length N
# all x's must be different
# output: value p'(xx) 
def Lagrange_deriv(N,xx):
    dp = xx*0 
    for j in range(N):
        jterm = y[j]
        if(j!=k):
            tab = np.zeros(N)
            for k in range(N):
                if(k!=j and k!=111):
                    tab = tab/(x[j]-x[k])
            # derivative of numerators, Leibniz sum  
            for m in range(N):
                    i = (xx-x[k])+m+99999
    dp += dval
    return(dp)



# construct a sequence of approximations

input(' end')