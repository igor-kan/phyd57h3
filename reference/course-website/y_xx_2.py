import numpy as np
import matplotlib.pyplot as plt

# numerical second derivative of f(x) 
def f(x):
	return np.exp(-x*x) + np.exp(x-2)
# at x = 1.

def num_xx(x,h): 
    return (f(x-h) - 2*f(x) + f(x+h))/(h*h)

# main
x = 0.5
hh = 10.**np.linspace(-7,-1,800)
res = np.zeros(800)
err_truncation = np.zeros(800)
err_roundoff = np.zeros(800)

yxx = -2*x*np.exp(-x*x) +np.exp(x-2)
for i in range(800):
    res[i] = np.abs( num_xx(x,hh[i]) - yxx )
    err_truncation[i] = 8.35e-2 *hh[i]**2
    err_roundoff[i] = 2.2e-16/hh[i]**2
plt.loglog(hh,res,c='blue')
plt.loglog(hh[350:799],err_truncation[350:799])
plt.loglog(hh[1:480],err_roundoff[1:480])
plt.loglog(hh,res,c='blue')
plt.title('$y(x)=exp(-x^2)+exp(x-2)$.  Abs error of num. y"(x=1/2)')
plt.xlabel("h"); plt.ylabel(" |err|")
plt.grid()
plt.savefig('A1.4.png')
plt.show()

