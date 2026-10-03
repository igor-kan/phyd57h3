import numpy as np
#import scipy as sp
import matplotlib.pyplot as plt
plt.interactive(True)



def f(x,y):     # dy/dx = f(x,y)
    return( -np.sin(x)*y )

def y_exact(x):
    return( np.exp(np.cos(x)-1) ) # by separ. of var.

'''  
    one time step of a 1-D ODE integration
    solve dy/dx = f(x,y) = -sin(x)*y  
    with boundary cond. y(0)=1, 
    & various integration schemes.
    
    function step() returns new x and y after step dx
    based on previous x,y and derivative dy/dx 
    given by function f(x,y)
'''
           
def step(scheme,x,y,dx):   
    dx_2 = dx/2     # half-step useful in many schemes
    f0 = f(x,y)     # beginning of step, subscript 0 
    x1 = x + dx     # after step dx, subscript 1    

    # different integration schemes
    if(scheme == -1):     # Euler 
        y1 = y + f0*dx 
    if(scheme == +1):     # Euler w/updated v
        y1_predict = y +f0*dx 
        y1 = y + f(x1,y1_predict)*dx  # backward Euler
    if(scheme == -2):     # 2nd order, trapezoid rule
        y1_predict = y +f0*dx 
        f1 = f(x1,y1_predict)
        y1 = y + (f0+f1)*dx_2  
    if(scheme == +2):     # midpoint x12
        x12 = x + dx_2
        y12_predict = y +f0*dx_2
        f12 = f(x12,y12_predict)
        y1  = y + f12*dx  
    if(scheme == +3):     # Simpsons-like formula 
        y1_predict = y +f0*dx # from trapezoidal
        f1 = f(x1,y1_predict) # from trapezoidal
        x12 = x + dx_2        # from midpoint
        y12_predict = y +f0*dx_2    # from midpoint
        f12 = f(x12,y12_predict)    # from midpoint
        y1  = y +(f0+4*f12+f1)/6*dx # 2/3 mid +1/3 trap
    if(scheme == +4):     # RK4 (Runge-Kutta 4th order)
        k1 = f0               # starting point
        x12 = x + dx_2        # midpoint
        k2 = f(x12,y+k1*dx_2) # midpoint slope, 1st approx
        k3 = f(x12,y+k2*dx_2) # midpoint slope, 2nd approx
        k4 = f(x1,y+k3*dx)    # endpoint slope, 1st approx
        y1 = y +(k1+2*(k2+k3)+k4)/6*dx # error-canceling mix
    return(x1,y1)

'''
    function integrate
    Integrates ODE with step dx=const, from compares many schemes:
    Euler, backward Euler, trapezoid, midpoint, RK4
    plot = 1 draws solutions
    plot = 2 shows convergence as dx-->0
    returns: final (ey), mean quadr. error (err), color
'''

def integrate(scheme,dx,plot=1):
# starting point and timestep   
    x, y = 0, 1 # initial conditions  
    col = (0,0,0)
    if(scheme == -1): col = (0,0,1)     # Euler
    if(scheme == +1): col = (0,.8,.3)   # bkw Euler
    if(scheme == -2): col = (1,0,.5)    # trapezoid
    if(scheme == +2): col = (0,0,0)   # midpoint
    if(scheme == +3): col = (.6,.6,.6)  # Simpson-like
    if(scheme == +4): col = (1,0,.5)   # Runge-Kutta 4
    if(plot==1): # plot first point
        plt.scatter(x,y,s=3,color=col,linewidth=0.5)
# integration from 0 to X, in max_steps intervals 
    X = np.pi*(39-19*plot)  # = 20*pi (plot=1) or pi (plot=2)
    max_steps = int(X/dx)
    if (abs(scheme) == 1): pwr = 0
    if (abs(scheme) > 1 ): pwr = 4+np.log10(2.)
    if (scheme == 4): pwr = 9
    err_norm = 10**pwr
    err = 0
    
    for i in range(max_steps):  # integration
# one step of integration updates x and y
        x,y = step(scheme,x,y,dx)
        ey = y - y_exact(x)  # local error
        err += ey*ey         # cumulative quadratic err
        if (plot==1 and i%4==0):
            if(i%40 == 0):
                print('%d %7.4f  %7.4f  %f' %(i,x,y,ey))
            plt.scatter(x,1+y,s=3,color=col,linewidth=0.5)
            offset = 
            plt.scatter(x,ey*err_norm+offset, s=2,color=col, \
                    alpha=0.5,linewidth=0.1)
            
    if (plot==1):
        xx = np.linspace(0,X*1.05,400)
        yy = 1+y_exact(xx) 
        plt.grid(True)
        plt.plot(xx,yy,linewidth=.66,color=(.9,.0,0))
        plt.show()
    err = (err/max_steps)**0.5
    ey = y - y_exact(x)
    print('scheme',scheme,'  dx=',dx,' mean-sq. err',err)
    print('%d %7.4f  %7.4f  y-y_exact %f' %(i,x,y,ey))
    if(plot<2):
        xpos = x+.1
        #if(abs(scheme)>1): xpos = 6.32
        #if(scheme==4): xpos = 5.15
        plt.text(xpos,ey*err_norm, \
            str(-np.around(np.log10(err_norm))))
        input(' ok?')
    return(ey,err,col)


'''
	Main program diff1-ex3.py
'''
plt.figure(dpi=140)
plt.xlabel('x')
plt.ylabel('1+y,   $(y-y_{theor})\cdot 10^{1,4,8}$')
plt.title(' ODE integration schemes of dy/dx = -cos(x)y')
# overplot results of different integration schemes 
p = 0
names =[' ','Euler','Euler(bkw)','trapezoid','midpoint',
       '2nd ord.~Simpson','Runge-Kutta 4th order',' ']
for scheme in [-1,+1,-2,+2,+3,+4]:
    dx0 = dx = 0.02
    p += 1
    plt.text(2.4,1-0.066*p,names[p])
    final_del_y,err,col  = integrate(scheme,dx,1)
    
input(' now the convergence study ')
plt.cla()
plt.figure(dpi=140)
plt.xlabel('$\log_{10} \Delta x$')
plt.ylabel('$\log_{10} \sqrt{<(y-y_{theor})^2>}$')
plt.title('mean error of solution to dy/x = -y cos(x),  x=0 to x=$\pi$',fontsize=10)
p = 0
for scheme in [-1,+1,-2,+2,+3,+4]:
    p += 1
    # plt.text(2.8,1-0.066*p,names[p])
    for k in range(18):
        dx = 0.256/2**k
        final_err,mean_err,col = integrate(scheme,dx,plot=2)
        logerr = np.log10(mean_err)
        logh   = np.log10(dx)
        plt.scatter(logh,logerr,s=4,color=col)
        plt.text(-5.6,-1.8-0.5*p,names[p])
    plt.show()
    input('ok? ')