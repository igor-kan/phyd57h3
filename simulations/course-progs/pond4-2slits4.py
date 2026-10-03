#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 14:56:03 2019
Solves the cylindrical surface wave Z(R,theta,t) 
on a surface-tension dominated pond of water:
    Z_tt = c^2 d2 Z / dt2 @author: pawel
"""

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np
import time


fig = plt.figure(figsize=(15,9))
ax = fig.add_subplot(111, projection='3d')

# Make the X, Y meshgrid.
N = 170
tendsim = 2.15

xs = np.linspace(-1, 1, N)
ys = np.linspace(-1, 1, N)
X, Y = np.meshgrid(xs, ys)
bump = 0.5 * np.exp(-((X+1.)**2+0*Y*Y)/0.05**2)
# initial conditions 
Z  = bump*0.
dV = bump*0
V  = dV*0
# set the z axis limits
ax.set_zlim(-1., 1.)
wframe = None
tstart = time.time()

dx = 2./N
# the longest time step allowed 
dt = dx/1. *0.5  # CLF number = 0.5, c = 1
num = int((tendsim)/dt)
print(num," steps, t_end=",tendsim," dt",dt)

# main time loop
for ist in range(0,num):
    t = dt*ist
    # remove it before drawing new one 
    if(ist%1==0):
        if (wframe):
            ax.collections.remove(wframe)

    # linear wave eq. on (x,y) grid, (c dt/dx)^2 = (N/2*dt)^2
    # 5-point stencil
    for i in range(1,N-1):
        for j in range(1,N-1):
            nabla2 = -4*Z[i,j]+Z[i-1,j]+Z[i+1,j]+Z[i,j-1]+Z[i,j+1]
            dV[i,j] = 0.25*nabla2
# von Neumann cond
    dV[0,:]   = dV[1,:]
    dV[N-1,:] = dV[N-2,:]
    dV[:,0]   = dV[:,1] 
    dV[:,N-1] = dV[:,N-2]
    
    V = V + dV    #dV is really dV/dt *dt
# von Neumann cond
#    V[0,:] = V[1,:]
#    V[N-1,:] = V[N-2,:]
#    V[:,0] = V[:,1] 
#    V[:,N-1] = V[:,N-2]
#
    Z = Z +  V    # V is really dZ/dt *dt
    
# periodic source of wave in the left half of the pool
    Z[0:1,:] = 0.5*np.sin(5*6.283*t)
# enforce zero disturbance inside object
    p1 = int(0.42*N)
    p2 = int(0.58*N)
    w = 2
    Z[2:2+2,    0:p1-w] = 0.
    Z[2:2+2, p1+w:p2-w] = 0.
    Z[2:2+2,     p2+w:] = 0.
   
# wireframe snapshot
# Plot the new wireframe and pause briefly before continuing.
#    Z = step (X, Y, Z, Z0, N, t, dt)        
    if(ist%1==0): 
        wframe = ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2, \
          color=(.2,.35,.35))
    plt.pause(.001)
print('Average FPS: %f' % (num / (time.time() - tstart)))
plt.pause(30.)
