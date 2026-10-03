#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 14:56:03 2019
Solves the cylindrical surface wave Z(R,theta,t) 
on a surface-tension dominated pond of water:
    Z_tt = c^2 (1/R) (R Z')' + forcing, where '=d/dR
@author: pawel
"""

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np
import time


fig = plt.figure(figsize=(15,9))
ax = fig.add_subplot(111, projection='3d')

# Make the X, Y meshgrid.
N = 120
tendsim = 25.0

xs = np.linspace(-1, 1, N)
ys = np.linspace(-1, 1, N)
X, Y = np.meshgrid(xs, ys)
bump = -0.75 * np.exp(-((X-0.3333)**2+Y*Y)/0.05**2)
# initial conditions 
Z  =  bump
dV = bump
V = dV*0
# set the z axis limits
ax.set_zlim(-1.1, 1.1)
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
    if(ist%2):
        if (wframe):
            ax.collections.remove(wframe)

    # linear wave eq. on (x,y) grid, (c dt/dx)^2 = (N/2*dt)^2
    # 5-point stencil
    for i in range(1,N-2):
        for j in range(1,N-2):
            nabla2 = -4*Z[i,j]+Z[i-1,j]+Z[i+1,j]+Z[i,j-1]+Z[i,j+1]
            dV[i,j] = 0.25*nabla2
    V = V + dV    #dV is really dV/dt *dt
    Z = Z +  V    # V is really dZ/dt *dt
# wireframe snapshot
# Plot the new wireframe and pause briefly before continuing.
#    Z = step (X, Y, Z, Z0, N, t, dt)        
    if(ist%2): 
        wframe = ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2, \
          color=(.15,.3,.4))
    plt.pause(.001)
print('Average FPS: %f' % (num / (time.time() - tstart)))
