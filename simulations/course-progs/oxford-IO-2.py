import numpy as np
import time
import matplotlib.pyplot as plt
#plt.interactive(True)

'''
    Number of sunny hours in Oxford, UK
    n = number of years, m = number of months each year = 12
'''
# read the array  
hrs = np.loadtxt("oxford.dat") # default is space-separated values 
n = len(hrs)   # len() only shows # of rows, size() would show # items
m = 12         # number of columns of data (monthly values) 

print(n,'years of data will be analyzed')
yax = 'number of sunny hours in Oxford'
xax = 'month'
plt.figure(figsize=[8.5,6])
plt.ylabel(yax)
plt.xlabel(xax)
plt.title('colors progress from green to red with the number of year')
yr = np.linspace(1,n,n).astype(int)     # array of year  numbers, 1..81
mo = np.linspace(1,m,m).astype(int)     # array of month numbers, 1..12

# long-tem average data
ratios = 0*hrs
aver   = hrs.sum(axis=0)/n  # table of 12 long-term averages
ratios = 0*hrs              # create ratios, hlp normalized to 81-year averages
yearly = hrs.sum(axis=1)/12 # table of 81 yearly averages

# print(n,'yearly averages:', yearly)
for month in range(12):
    ratios[:,month] = hrs[:,month]/aver[month]

# loop over years while plotting
for y in yr:
    c = (y+1)/(n+1)
    rgb = (c*c, 1-c, 2*c*(1-c))   # color according to year
    xs = mo+(y-40)/300
    plt.scatter(xs,hrs[y-1,:],s=16,color=rgb,linewidth=1)
plt.plot(mo,aver)
plt.show()

#  second, renormalized plot

txt = 'values normalized to monthly averages'
plt.figure(figsize=[8.5,6])
plt.ylabel(yax)
plt.xlabel(xax)
plt.title('# clear days normalized to averages')
plt.plot(mo,aver*0+1)           # plot average line ==1
for y in yr:
    c = (y+1)/(n+1)
    rgb = (c*c, 1-c, 2*c*(1-c)) # color according to year
    xs = mo+(y-40)/300          # position according to month but also year
    plt.scatter(xs,ratios[y-1,:],s=16,color=rgb,linewidth=1)
plt.show()
txt = "values"

plt.figure(figsize=[8.5,6])
plt.ylabel('yearly averages')
plt.xlabel('year')
plt.title(' yearly averages with error bars')
#plt.plot(yr,yearly)
plt.scatter(yr,yearly,s=9,color=(0,0,1),linewidth=1)
# compute error bars (sigma of the yearly mean)
diff2 = np.zeros(n)
print(' shapes', yearly.shape, diff2.shape, ' yr[-1] = ',yr[-1])
for i in range(12):
    diff2 += (hrs[:,i]-yearly)**2
sigma_mean = (diff2/11/12)**0.5 
plt.errorbar(yr,yearly,yerr=sigma_mean,ecolor=(1,.4,.7),barsabove=True)
plt.show()

