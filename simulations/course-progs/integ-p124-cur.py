import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive, cm
from time import time
interactive(True)

# integrate 

def f(x):
    dydx = B*np.cos(2*np.pi*x)
    return((1.+dydx*dydx)**0.5)

def dL(x,dx):
    y0 = 0.4*np.sin(2*np.pi*x)
    y1 = 0.4*np.sin(2*np.pi*(x+dx))
    return((dx*dx+(y1-y0)**2)**0.5)


'''
    Euler(left)
'''
def Euler_L(a,b,N):
    sum, h = 0, (b-a)/N
    for i in range(N):
        x = a + h*i  # left boundary of x interval i
        y = f(x)
        sum += y        
    L = 24*sum*h
# integration completed
    logh = np.log10(h)
    if(L == L_exact):
        logerr = -16.5
    else: 
        logerr = np.log10(abs(L-L_exact))
    plt.scatter(logh,logerr,s=9,color=(0,.3,1),alpha=0.5)

'''
    Euler(dL)
'''
def Euler_dL(a,b,N):
    sum, h = 0, (b-a)/N
    for i in range(N):
        x = a + h*i  # left boundary of x interval i       
        sum += dL(x,h)
    L = 24*sum
# integration completed
    logh = np.log10(h/2)
    if(L == L_exact):
        logerr = -16.5
    else: 
        logerr = np.log10(abs(L-L_exact))
    plt.scatter(logh,logerr,s=9,color=(1,0,1),alpha=0.5)
     
    
'''
    trapezoid rule
'''
def trapezoid(a,b,N):
    sum, h = 0, (b-a)/N
    for i in range(1,N):
        x = a + h*i  # left boundary of x interval i
        sum += f(x)
    sum += (f(a)+f(b))/2
    L = 24*sum*h
# integration completed
    logh = np.log10(h)
    if(L == L_exact):
        logerr = -16.5
    else: 
        logerr = np.log10(abs(L-L_exact))
    plt.scatter(logh,logerr,s=9,color=(1,0,0),alpha=0.6)
    
 
'''
    midpoint rule
'''
def midpoint(a,b,N):
    sum, h = 0, (b-a)/N
    for i in range(N):
        x = a + h*(i+0.5)  # center of x interval i
        sum += f(x)  
    L = 24*sum*h
# integration completed
    logh = np.log10(h)+0.0166
    if(L == L_exact):
        logerr = -16.5
    else: 
        logerr = np.log10(abs(L-L_exact)) 
    plt.scatter(logh,logerr,s=9,color=(.25,.75,0),alpha=0.7)
    
'''
    Simpsons 1/3 rule
'''
def Simpson(a,b,N):
    sum, h = 0, (b-a)/N
    for i in range(N+1):
        x = a + h*i  # left boundary of x interval i
        y = f(x)
        c = (2+2*(i%2))  # 2,4,2,4,..,2  for i=1,2,3,4..,N
        if(i==0 or i==N): 
            c = 1
        sum += c*y
    L = 24*sum*h/3
# integration completed
    logh = np.log10(h)
    if(L == L_exact):
        logerr = -16.5
    else: 
        logerr = np.log10(abs(L-L_exact))
    plt.scatter(logh,logerr,s=9,color=(.4,.4,.4),alpha=0.5)
      


'''
    main (driver) program
    integrate the length of the curtain
    I = 24 * int_0^0.25 sqrt(1+B^2*cos^2(2*pi*x))
    where B = 2 pi (0.4/1.0), 0.4 - amplitude of wave, 1.0 wavelength
'''
  
from scipy.special import ellipe
plt.figure(dpi=140)
B = 2*np.pi*0.4
L_exact = ellipe(B*B/(1+B*B)) *12*(1+B*B)**0.5/np.pi
print(' exact L=',L_exact)

xL, xR = 0., 0.25

#plot integrated function
xx = np.linspace(0,0.25,100)
h = 0.25/100
plt.plot(xx,f(xx))
plt.plot(xx,dL(xx,h)/h,color=(1,0,0))
plt.title('integrated function is dL/dx for curtain problem')
plt.xlabel('x/$\lambda$')
plt.ylabel(' dL/dx = $\sqrt{1+B^2 \cos^2 2\pi x}$')
plt.show
input(' function plot done. next?')
plt.cla
plt.figure(dpi=140)

# all methods
for p in range(200):
    N = 2*p+2 # even N required by Simpson's rule
    Euler_L  (xL,xR,N)
    midpoint (xL,xR,N)
    trapezoid(xL,xR,N)
    Simpson  (xL,xR,N)
    Euler_dL (xL,xR,N)
plt.title("Convergence of integration of curtain's length")
plt.xlabel('log$_{10}$ h')
plt.ylabel('log |L - L$_{exact}$|')
plt.grid
plt.text(-3,-7,'blue = Euler')
plt.text(-3,-8,'green = midpoint')
plt.text(-3,-9,'red = trapezoid')
plt.text(-3,-10,"grey = Simpson 1/3")
plt.text(-3,-11,"magenta = Pythagoras")
# +2, +4 slope lines
xx = np.linspace(-3.5,-1,100)
plt.plot(xx,2*xx+1.5,color=(.6,.6,.7),alpha=0.4)
plt.plot(xx,4*xx+3.,color=(.7,.7,.8),alpha=0.4)
plt.plot(xx,1*xx+0.9,color=(.7,.7,.8),alpha=0.4)
#plt.plot(xx, -xx-16.5,color=(.7,.7,.8),alpha=0.5)
plt.plot(xx,-xx/2-15.1,color=(.8,.8,.8),alpha=0.6)
plt.show()
input('comparison done. go on? ')