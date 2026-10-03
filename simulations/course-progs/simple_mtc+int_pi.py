import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)
'''
  Pi by MteCarlo vs. 1st order integration of circle
  with the same number of points. 
'''


def MteCarlo(N):
# in N experiments, sum three dice 
    xr = np.random.rand(N)      # rnd float array
    yr = np.random.rand(N)      # rnd float array
# plot a quarter circle  
    xx = np.linspace(0,1,N)
    yy = np.sqrt(1-xx*xx)
# compute pi by trapezoid rule (2nd order integration)
    subtr = yy[0]/2 + yy[N-1]/2
    integ1_pi =  yy.sum()        *(xx[1]-xx[0])*4 
    integ2_pi = (yy.sum()-subtr) *(xx[1]-xx[0])*4 
# now MteCarlo
    plt.figure(figsize=[7,6.5])
    p = plt.plot(xx,yy)
    plt.axis(limits=[-.3,1.3,0,1])
    inside = xr*xr+yr*yr < 1.0   # Bolean arr
    co = inside.astype(int)      # cast Boolean as int
    mypi = co.sum()/N *4
    sig  = N**(-0.5)*mypi        # expected std/mypi = N**(-1/2)
    
    # LaTeX style text
    label = str(np.around(mypi,5))+' + '+ \
        str(np.around(np.pi-mypi,5))+' ('+ \
        str(np.around(sig,5))+')  Monte Carlo, N =  '+str(N) 
    logN = np.log10(N)  #  needed only for nicer plotting
    if (logN > 5.5): 
        xr = xr[0:200000]; yr = yr[0:200000]; co = co[0:200000]
    plt.scatter(xr,yr, s=7-logN//2, c=255-co*100, 
                alpha=0.95-logN*.05)
    plt.xlabel('X') 
    plt.ylabel('Y')
    plt.title ('$\pi = $'+label)
    plt.grid(True)
    print("MtC integration ",mypi,     '+',np.pi-mypi, ' N = ',N)
    print("integr. 1st ord ",integ1_pi,'+',np.pi-integ1_pi)
    print("integr. 2nd ord ",integ2_pi,'+',np.pi-integ2_pi) 
	return(None)
# end of function 


'''
 Main (driver) program
 Notice a well stuctured, functional programmig style: 
 rather small driver program including interaction with user
 and a self-sufficient function that is called for different N.
 With many functions, it is easier to test them with this style.
 All the output is handled by the function. The function thus 
 does not return any values. We make this explicit by the 
 optional return statement returning nothing. 
'''  
for n in range(1,7):
    N = 10**n
    MteCarlo(N)
    input(" next? ")
plt.close()
