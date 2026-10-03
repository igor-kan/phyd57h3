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


def step (X, Y, Z, Z0, N, t, dt):
# linear wave eq. on (x,y) grid, c^2 = 1.0
    for i in range(1,N-2):
        for j in range(1,N-2):
            nabla =  Z[i-1,j] + Z[i+1,j] +  \
                     Z[i,j-1] + Z[i,j+1] - 4*Z[i,j]
            newZ = 2*Z[i,j] + Z0[i,j] + nabla
            Z0[i,j] = Z[i,j]  # update Z0
            Z[i,j] = newZ 
    return Z, Z0


fig = plt.figure(figsize=(10,6.66))
ax = fig.add_subplot(111, projection='3d')

# Make the X, Y meshgrid.
N = 120
xs = np.linspace(-1, 1, N)
ys = np.linspace(-1, 1, N)
X, Y = np.meshgrid(xs, ys)
bump = -0.5 * np.exp(-(X*X+Y*Y)/0.08**2)
# initial conditions, depression near center
Z  =  bump
Z0 =  bump*1.0001

# Set the z axis limits so they aren't recalculated each frame.
ax.set_zlim(-1.2, 1.2)

# Begin plotting.
wframe = None
tstart = time.time()
tendsim = 2.0
dt = 0.001
num = int((tendsim)/dt)


# time loop
for ist in range(0,num):
    t = dt*ist
    # If a line collection is already remove it before drawing.
    if wframe:
        ax.collections.remove(wframe)

    # Plot the new wireframe and pause briefly before continuing.
#    Z = step (X, Y, Z, Z0, N, t, dt)   
    # linear wave eq. on (x,y) grid, (c dt/dx)^2 = (N/2*dt)^2
    # 5-point stencil
    dx = 2./N
    cdt_dx_2 = min((dt/dx)**2, 0.1)
    for i in range(1,N-2):
        for j in range(1,N-2):
            nabla =  Z[i-1,j] + Z[i+1,j] +  \
                     Z[i,j-1] + Z[i,j+1] - 4*Z[i,j]
            newZ = 2*Z[i,j] - Z0[i,j] + cdt_dx_2*nabla
            Z0[i,j] = Z[i,j]  # update Z0
            Z[i,j] = newZ 
    
    wframe = ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2, \
          color=(.15,.3,.4))
    plt.pause(.0001)

print('Average FPS: %f' % (num / (time.time() - tstart)))
