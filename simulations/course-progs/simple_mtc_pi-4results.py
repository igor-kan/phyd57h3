'''
Plot results of simple_mtc+3int_pi.py
'''
import numpy as np
import matplotlib.pyplot as plt
plt.interactive(True)
x = [1,2,3,4,5,6,7]
resMC1 = np.array([-0.4947,-0.10593,0.0207,0.005106,-0.0004959, -0.0005442,0.0002965])
resMC2 = np.array([-0.16292,-0.0267,-0.11115,0.0031065,-0.00225,0.005467, -0.000626])
resMC3 = np.array([-0.1311,-0.22474,-0.0751,0.01350,0.00386,0.0001957,0.0003521])
res2nd = np.array([0.0371, 0.001176,3.718e-05,1.176e-06,3.718e-08,1.176e-09,3.719e-11])
res3rd = np.array([.01458,.0004595,1.4523e-05,4.5925e-07,1.452e-08,4.593e-10,1.434e-11])
plt.figure(figsize=[8,6])
plt.scatter(x,np.log10(abs(res2nd)),s=4,linewidth=4,alpha=0.7)
plt.scatter(x,np.log10(abs(res3rd)),s=4,linewidth=4,alpha=0.7)
plt.grid(True)
plt.show()

ans = input("next?")
 
plt.scatter(x,np.log10(abs(resMC1)),s=12,linewidth=3,alpha=0.7)
plt.scatter(x,np.log10(abs(resMC2)),s=12,linewidth=3,alpha=0.7)
plt.scatter(x,np.log10(abs(resMC3)),s=12,linewidth=3,alpha=0.7)
plt.title("Error in $\pi$ calculation")
plt.xlabel("log N ")
plt.ylabel("log$_{10}$|err|")
plt.text(3.1,-9,"integration of area, dx=1/N")
plt.text(4.3,-1,"Monte Carlo calculations")
plt.text(4.3,-1.6,"slope = -1/2  (error$\sim N^{-1/2}$)")
plt.plot([1,7],[-0.5,-3.5],alpha=0.4)
plt.plot([1,7],[-1.4,-10.4],alpha=0.4)
plt.grid(True)
plt.show()

# equivalent function:  np.random.normal(size=N)

ans = input("next?")
