import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive, cm
from time import time
interactive(True)

# integrate 

def f(x):  
    f = 1./(1.+x*x)
    return(f)

'''
    Euler(left)
'''
def Euler_L(a,b,N):
    sum, h = 0, (b-a)/N
    for i in range(N):
        x = a + h*i  # left boundary of x interval i
        sum += f(x)       
    L = sum*h
# integration completed
    logh = np.log10(h)
    if(L == L_exact):
        logerr = -16.5
    else: 
        logerr = np.log10(abs(L-L_exact))
    plt.scatter(logh,logerr,s=9,color=(0,.3,1),alpha=0.5)
    
    
'''
    trapezoid rule
'''
def trapezoid(a,b,N):
    sum, h = 0, (b-a)/N
    for i in range(1,N):
        x = a + h*i  # left boundary of x interval i
        sum += f(x)
    sum += (f(a)+f(b))/2
    L = sum*h
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
    L = sum*h
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
        c = 2+2*(i%2)  # 2,4,2,4,..,2  for i=1,2,3,4..,N
        if(i==0 or i==N): 
            c = 1
        sum += c*y
    L = sum*h/3
# integration completed
    logh = np.log10(h)
    if(L == L_exact):
        logerr = -16.5
    else: 
        logerr = np.log10(abs(L-L_exact))
    plt.scatter(logh,logerr,s=9,color=(.5,.5,.5),alpha=0.8)
      




'''
    main (driver) program
    integrate the length of the curtain
    I = 24 * int_0^0.25 sqrt(1+B^2*cos^2(2*pi*x))
    where B = 2 pi (0.4/1.0), 0.4 - amplitude of wave, 1.0 wavelength
'''
  

plt.figure(dpi=140)
 
L_exact = np.pi/4
print(' exact L=',L_exact)

xL,xR = 0,1

#plot integrated function
xx = np.linspace(0,1,200)
plt.plot(xx,f(xx))
plt.title('integrated function')
plt.xlabel('x')
plt.ylabel(' $y(x) = 1/(1+x^2)$')
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
plt.title("Convergence of integration methods of $(1+x^2)^{-1}$")
plt.xlabel('log$_{10}$ h')
plt.ylabel('log |I - $\pi$/4|')
plt.grid
plt.text(-1.3,-12,'blue = Euler')
plt.text(-1.3,-13,'green = midpoint')
plt.text(-1.3,-14,'red = trapezoid')
plt.text(-1.3,-15,"grey = Simpson 1/3")
# +2, +4 slope lines
xx = np.linspace(-2.5,-0.5,100)
plt.plot(xx,2*xx-1,color=(.6,.6,.7),alpha=0.4)
plt.plot(xx,4*xx-2,color=(.7,.7,.8),alpha=0.4)
plt.plot(xx,1*xx-.5,color=(.7,.7,.8),alpha=0.4)
plt.plot(xx,6*xx-1.5,color=(.7,.7,.8),alpha=0.4)
plt.plot(xx,0*xx-15.9,color=(.9,.9,.8),alpha=0.4)
plt.text(-2.,-2.1,'$h^1$')
plt.text(-2.,-5.,'$h^2$')
plt.text(-2.,-9.5,'$h^4$')
plt.text(-1.75,-11.8,'$h^6$')
plt.text(-1.8,-15.5,'machine $\epsilon$',color=(.7,.7,.8),alpha=0.75)

plt.show()
input('comparison done. go on? ')