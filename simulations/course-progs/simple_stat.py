'''
    Simple file I/O for ASCII data.
    Prepare data for simple statistics exercise
    Store, Read, do statistics in 3 different ways
'''
import numpy as np
import matplotlib.pyplot as plt
plt.interactive(True)

N = 100
# data generation 

x = np.linspace(0,10,N)
y = 100+np.sin(x)-(x/10)**2+(x/10)**4   # some function
y = y +1.5*np.random.randn(100)         # add fuzz, sigma=1.5
print(" sig",np.random.randn(100).std())
tab = np.zeros((2,100),dtype=float) 
tab[0,:] = x  # this will be column 1 in the file, now it's row 1
tab[1,:] = y  # this will be column 2 in the file, now it's row 2

# plotting
plt.figure(figsize=[9,6])
plt.plot(x,y,linewidth=1)
plt.plot(x,y,'bo')
plt.title(" Time series of measurements")
plt.show()
input(" next? ")

# store data in file with space-separated values (e.g., .dat)
np.savetxt("simple_io.dat",tab.T)  # transpose rows into columns & store
# store data in file with space-separated values (.csv)
np.savetxt("simple_io.csv",tab.T,delimiter=",")

# read data from file of space-separated values 
xx,yy = np.loadtxt("simple_io.dat",delimiter=" ").T
# or like this (space delimiter is a defult)
xx,yy = np.loadtxt("simple_io.dat").T

# this will also work too
xx,yy = np.loadtxt("simple_io.csv",delimiter=",").T
# but this will not (because the default separator is space)
#zz,ww = np.loadtxt("simple_io.csv").T
# this will fail as well
#aa,bb = np.loadtxt("simple_io.dat",delimiter=",").T

'''
 simple statistics on data
'''
#
# mean and std deviation 
# < > = arithmetic average or sum divideb by numer of items
# mean of y_i is <y> := (1/N) Sum_0^{N-1} y[i] 
# std deviation 
# sigma := 1/(N-1) * Sum_0^{N-1} (y[i]-<y>)**2 = N/(N-1) <(y - <y>)^2> =
#        = N/(N-1) [ <y**2> - <y>**2 ]

# method 1
y_ave = y2_av = 0.
for i in range(N):
    y_ave += yy[i]
    y2_av += yy[i]**2
y_ave = y_ave/(N-1) 
y2_av = y2_av/(N-1)

var_1 = y2_av - y_ave**2 
sigm_a = (var_1/N)**(1/2)
print("method 1: ",y_ave,'+-',sigm_a,' sigma=',var_1**0.5)

y_ave = yy.sum()/N
var_2 = np.sum((yy-y_ave)**2)/N  
sigm_a = (var_2/N)**(1/2)
print("method 2: ",y_ave,'+-',sigm_a,' sigma=',var_2**0.5)

y_ave  = yy.mean()
stdev = yy.std()
sigm_3 = stdev/N**(1/2)
print("method 3: ",y_ave,'+-',sigm_3,' sigma=',yy.std())

# plot data after statistics is done
# plt.plot(xx,yy,linewidth=1,color='y')
# overplot
#plt.text(xx[7],104.,'$\sigma$ and $\simga_m$ bands shown')
plt.figure(figsize=[9,6])
plt.title(' <y> $\pm \sigma_m$, and $\sigma$ shown as bands. Approx. 16+16 points are expected outside $\pm\sigma$')
plt.plot(xx,yy*0+y_ave,       linewidth=1,  color='k')
plt.plot(xx,yy*0+y_ave+sigm_3,linewidth=0.5,color='k')
plt.plot(xx,yy*0+y_ave-sigm_3,linewidth=0.5,color='k')
plt.plot(xx,yy*0+y_ave+stdev,linewidth=0.5,color=(.3,.3,1))
plt.plot(xx,yy*0+y_ave-stdev,linewidth=0.5,color=(.3,.3,1))
plt.text(1.5,y_ave+stdev+.3,
         '+standard dev. $\sigma$',fontsize=14)
plt.text(1.5,y_ave-stdev-.4,
         '-standard dev. $\sigma$',fontsize=14)
plt.scatter(xx,yy,linewidth=2,color=(0.66,0,0))
plt.show() 
input(" next? ")
