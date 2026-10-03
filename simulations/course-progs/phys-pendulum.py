"""
    Physical pendulum of unit length, analysed with Leapfrog
   
"""

import numpy as np
from numpy import sin,cos
import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

T = 100*(np.pi*2)
dt = 0.001
num_steps = int(T/dt)
skip = num_steps//500 
phi0 = 177        # deg,  initial deflection angle of pendulum

# save positions in
xs = np.empty(num_steps+1)
vs = np.empty(num_steps+1)
ts = np.empty(num_steps+1)
errs = np.empty(num_steps//skip+1)
# Set initial values

phi = np.pi/180. * phi0   # rad
print("initial position",phi,"  at rest.")
vphi  = 0.              # rad/s, but since r=1, also m/s
g = 9.81                # m/s**2 
t = 0.                  # s
# Step through time, calculating the derivatives
# and updating variables. Leapfrog integration scheme,
# though it's a bit hard to recognize
q = 0.5
for i in range(num_steps+1):
    t = t + dt             # update time
    # save phi and vphi for a later plot
    xs[i]  = phi/np.pi*180;   vs[i]=vphi;   ts[i]=t
    # potential en. divided by mass, U = -g*cos(phi), 
    # so we have -dU/d(phi) = phi'' = -g sin(phi)
    # which is pendulum's equation of motion.
    accphi = -g * sin(phi)  # acceleration (d^2{phi}/dt^2) of phi 
    vphi = vphi + dt*accphi*q # velocity update before position update
    phi  =  phi + dt*vphi
    q = 1
    # error of energy (phi and vphi must be synchronized correctly)
    if (i%skip == 0):      # no need to do it often; here, ever 20th step
        phi_syn = phi -dt*vphi/2
        U = g*(1-cos(phi_syn))  # potential energy/mass, zero at phi=0
        v = vphi         # since r=1, v (linear speed) = r*dphi/dt = vphi
        K = v*v/2        # K = kinetic energy/mass
        E = U + K        # total energy/mass
        if (i==0):       # save initial energy for comparison 
            E0 = E       # with later values of E
        errs[i//skip] = (E-E0)/E0  # save energy
# Plot
fig = plt.figure(dpi=140)
m = num_steps//20
plt.scatter(ts[0:0],xs[0:0],marker='.',c='b')
plt.plot(ts[0:m],xs[0:m])
plt.plot(ts[0:m],vs[0:m]*15,lw=0.5,c='r')
plt.xlabel('time [s]')
plt.ylabel('$\phi(t) [^o], \;\;\;  d\phi/dt * 15$')
plt.grid(True)
plt.title("Physical pendulum starting from $\phi(0)=$"+str(phi0)+"$^o$")
plt.text(7.1,168,'dt ='+str(dt))
plt.show()
#
plt.figure(dpi=130)
plt.xlabel('time [s]')
plt.ylabel('dE / E$_0$')
plt.grid(True)
tt = np.linspace(0,T,len(errs))
plt.plot(tt,errs)
plt.show()