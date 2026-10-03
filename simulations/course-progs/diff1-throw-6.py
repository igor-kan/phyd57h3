import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
plt.interactive(True)

'''  
    one time step of simulation
    2nd order scheme 
'''
  
def step(mode,t,vx,vz,x,z):
    vxp, vzp = vx, vz
    if(mode==1): 
        drag = c_drag *(vx*vx+vz*vz)**0.5
    else:
        drag = 0
    ax = -drag * vx
    az = -drag * vz + g
    vx = vx + ax*dt
    vz = vz + az*dt 
    x = x + 0.5*(vx+vxp)*dt
    z = z + 0.5*(vz+vzp)*dt
    return(vx,vz,x,z)


'''
	Main program diff1-throw-6.py
    Simulation of a throw of ball (5cm, density of water)
    in vacuum vs. in air 
    drag acceleration = -Cd v|v|/2 rho A/M
    (x0,z0) = (0,0)  &  (vx0,vz0) = (50,20) m/s
'''
plt.figure(dpi=140)

g = -9.81         # m/s/s
Cd = 0.47
R = 0.05          # m
A = np.pi * R**2
rho = 400.        # 0.4 density of water
M = (4/3)*np.pi*R**3*rho # kg 
c_drag400 = Cd *1.26/2*A/M  # accel = c_drag * V^2 (rho_air=1.25 kg/m^3)


c_drag = 0
t, dt = 0, 0.08   # s 
vx = vx0 = 70.    # m/s
vz = vz0 = 25.    # m/s
x,z = 0, 0        # m
plt.scatter(0,0,s=5,color=(0,0,1),linewidth=0.6)

for i in range(int(-2*vz0/g/dt)+1):
    t += dt
    vx,vz,x,z = step(0,t,vx,vz,x,z)
    z_th = vz0*t +g*t*t/2
    delz = z - z_th
    print(' %7.4f  %7.4f %7.4f %f' %(t,z,vz,delz))
    plt.scatter(x,z,s=5,color=(0,0,1),linewidth=0.7)
    if(z < 0): 
        az = g 
        T = t -vz/az+((vz/az)**2-2*z/az)**0.5
        print('T(no drag)',T,' T/T(theor)',T/(-2*vz0/g))
        break
plt.grid()
plt.xlabel('x [m]')
plt.ylabel('z [m]')
plt.title('throw v$_{0}$=('+str(vx0)+','+str(vz0)+ \
          ') m/s,   dt='+str(dt)+' s')
tt = np.linspace(0,T,400)
xx = tt*vx0
zz = vz0*tt + g*tt*tt/2  
plt.plot(xx,zz,linewidth=0.66,color=(0.8,0.5,0))
plt.text(220,20.1,'in vacuum')
plt.show()
input(' ok?')


c_drag = c_drag400/3 
t, dt = 0, 0.08   # s 
vx = vx0 = 70.     # m/s
vz = vz0 = 25.    # m/s
x,z = 0,0         # m
for i in range(int(-2*vz0/g/dt)+1):
    t += dt
    vx,vz,x,z = step(1,t,vx,vz,x,z)
    print('%7.4f  %7.4f %7.4f %7.4f' %(x,z,vx,vz))
    plt.scatter(x,z,s=5,color=(0,.75,0),linewidth=0.7)
    if(z < 0): 
        az = g -c_drag *(vx*vx+vz*vz)**0.5 * vz 
        T = t -vz/az+((vz/az)**2-2*z/az)**0.5
        print('T with drag*2. ',T,' T/T(0 drag)',T/(-2*vz0/g))
        break
plt.text(192,5.2,'$rho=1200$')
plt.show()
input(' ok?')

 
c_drag = c_drag400 
t, dt = 0, 0.08   # s 
vx = vx0 = 70.     # m/s
vz = vz0 = 25.    # m/s
x,z = 0,0         # m
for i in range(int(-2*vz0/g/dt)+1):
    t += dt
    vx,vz,x,z = step(1,t,vx,vz,x,z)
    print('%7.4f  %7.4f %7.4f %7.4f' %(x,z,vx,vz))
    plt.scatter(x,z,s=5,color=(1,0,0),linewidth=0.7)
    if(z < 0): 
        az = g -c_drag *(vx*vx+vz*vz)**0.5 * vz 
        T = t -vz/az+((vz/az)**2-2*z/az)**0.5
        print('T with drag*2. ',T,' T/T(0 drag)',T/(-2*vz0/g))
        break
plt.text(50,3,'$rho=400$')
plt.show()
input(' ok?')

