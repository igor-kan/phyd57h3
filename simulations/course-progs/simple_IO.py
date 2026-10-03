'''
    Simple file I/O for ASCII data
    Not memory-efficient, use it only for moderate amount 
    of data (kB, MB, but not not 100s of MB or GBs)
    [Python can store data more efficiently as 
    binary data in files!]
'''
from numpy import zeros, array, linspace, loadtxt, savetxt, sin
import matplotlib.pyplot as plt
plt.interactive(True)

x = linspace(0,10,100)
y = sin(x)-(x/10)**3 +3*(x/10)**4   # a math function
tab = zeros((2,100),dtype=float) 
tab[0,:] = x  # this will be column 1 in the file, now it's row 1
tab[1,:] = y  # this will be column 2 in the file, now it's row 2
plt.plot(x,y)
plt.title(' Plot 1, data to be stored, read back into RAM')
plt.show();  input(" next plot? ")

# store data in file with space-separated values (e.g., .dat)
savetxt("simple_io.dat",tab.T)  # transpose to turn rows into columns & store
# store data in file with space-separated values (.csv)
savetxt("simple_io.csv",tab.T,delimiter=",")

# read data from file of space-separated values 
xx,yy = loadtxt("simple_io.dat",delimiter=" ").T
# or like this (space delimiter is a defult)
xx,yy = loadtxt("simple_io.dat").T
print(xx)
print(yy)
plt.plot(xx,yy)
plt.title(' Plot 2, same values after IO operations.')
plt.show();  input(" next plot? ")

# this will work:
xx,yy = loadtxt("simple_io.csv",delimiter=",").T
print(" ##### success up to here #### ")
# but this will not (because the default separator is space)
zz,ww = loadtxt("simple_io.csv").T

# this will fail as well
aa,bb = loadtxt("simple_io.dat",delimiter=",").T