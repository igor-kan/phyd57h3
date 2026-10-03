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
    integ1_pi = yy.sum() *(xx[1]-xx[0])*4 
# now MteCarlo
    plt.figure(figsize=[7,6.5])
    p = plt.plot(xx,yy)
    plt.axis(limits=[-.3,1.3,0,1])
    inside = xr*xr+yr*yr < 1.0   # Bolean arr
    co = inside.astype(int)
    mypi = co.sum()/N *4
    sig  = N**(-0.5)*mypi
     # LaTeX style text
    label = str(np.around(mypi,5))+' + '+ \
        str(np.around(np.pi-mypi,5))+' ('+ \
        str(np.around(sig,5))+')  Monte Carlo, N =  '+str(N) 
    logN = np.log10(N)  #  needed only for nicer plotting
    plt.scatter(xr,yr, s=7-logN//2, c=255-co, alpha=0.95-logN*.05)
    plt.xlabel('X') 
    plt.ylabel('Y')
    plt.title ('$\pi = $'+label)
    plt.grid(True)
    print("MtC integration  "+label)
    print("integr. 1st ord ",integ1_pi,' + ', -integ1_pi+np.pi)
# main (driver) program
for n in range(1,6):
    N = 10**n
    MteCarlo(N)
    input(" next? ")
    #plt.cla()
    
plt.close()