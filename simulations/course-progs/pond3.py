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


fig = plt.figure(figsize=(10,6.66))
ax = fig.add_subplot(111, projection='3d')

# Make the X, Y meshgrid.
N = 100
xs = np.linspace(-1, 1, N)
ys = np.linspace(-1, 1, N)
X, Y = np.meshgrid(xs, ys)
bump = -1.2 * np.exp(-(X*X+Y*Y)/0.08**2)
# initial conditions 
Z  =  bump
Z0 =  bump
newZ = bump

# Set the z axis limits so they aren't recalculated each frame.
ax.set_zlim(-1.1, 1.1)

# Begin plotting.
wframe = None
tstart = time.time()
tendsim = 8.0
dx = 2./N
dt = dx/1. *0.5  # CLF number = 0.5
num = int((tendsim)/dt)
print(num," steps, t_end=",tendsim)
# time loop
cdt_dx_2 = min((dt/dx)**2, 0.5)
cnst = 2.-cdt_dx_2*4.  # = zero!
    
for ist in range(0,num):
    t = dt*ist
    # remove it before drawing new one
    if(ist%2):
        if (wframe):
            ax.collections.remove(wframe)

    # Plot the new wireframe and pause briefly before continuing.
#    Z = step (X, Y, Z, Z0, N, t, dt)   
    # linear wave eq. on (x,y) grid, (c dt/dx)^2 = (N/2*dt)^2
    # 5-point stencil

    for i in range(1,N-2):
        for j in range(1,N-2):
            nabla2_ = Z[i-1,j]+Z[i+1,j]+Z[i,j-1]+Z[i,j+1]
            newZ[i,j] = - Z0[i,j] + 0.5*nabla2_
    Z0 = Z
    Z = newZ
  #  Z0 = Z      # update Z0
  #  Z  = newZ   # update Z
# wireframe snapshot     
    if(ist%2): 
        wframe = ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2, \
          color=(.15,.3,.4))
    plt.pause(.001)
print( cdt_dx_2," = cdt_dx_2;  t=",t)
print('Average FPS: %f' % (num / (time.time() - tstart)))
