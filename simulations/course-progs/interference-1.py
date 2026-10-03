import numpy as np
import matplotlib.pyplot as plt
plt.interactive(True)


     


'''
	Main program interference-1.py
    
    Compute the diffracion pattern from sigle slit
    
    X = 15e-6          - half-width of the slit
    S = 120e-6          - half of the spacing between slits 
    lambda = 0.6e-6 m  - red light wavelength
    z = 1 m            - distance to screen
    y                  - coordinte on the screen
    Range of y:  approx. -6 to +6 cm,
    Compute only for y>0, use symmetry.
    Also, try to use vector operations on arrays,
    and np.sum() summation, 
    this will greatly speed up the integration
    
    Formula for intensity I(y) on the screen:
    I(y) = |f(y)|^2,   where f(y) is a complex-valued sum 
    f(y) = (z^2+y^2)^{-1/2} integral_{-X}^{+X} exp[i*k*delta(x)] dx, 
    delta = sqrt(z^2+(y-x-s)^2) - z
    s = -S or S (left or right slit)
    k = 2 pi / lambda 
    i = 1j in Python = imaginary unit
    Use 1001 points both on the screen and across the slit
'''

plt.figure(dpi=140)
X, Y, S, lamb, z = 15e-6, 0.06, 120e-6, 0.6e-6, 1. 
k = 2*np.pi/lamb        # wave number
ik = 1j * k
z2 = z*z
N = 1001
x = np.linspace(-X,X,N); dx = x[1]-x[0]
y = np.linspace(-Y,Y,N)
I = y*0   # initialize intensity array I(y)

# fill I(y) array
for l in range(N//2): 
    yy = y[N//2+l]
    deltas_L = (np.sqrt(z2+(yy-x+S)**2) - z)  #  N floats
    deltas_R = (np.sqrt(z2+(yy-x-S)**2) - z)  #  N floats
    integral = np.sum(np.exp(ik*deltas_L)+np.exp(ik*deltas_R))*dx
    f = integral/(z2+yy**2)**0.5
    intens = abs(f)**2
    I[N//2+l] = intens
    I[N//2-l] = intens
I = I/I.max()
# output
plt.plot(100*y,I)
plt.plot(100*y,y*0,linewidth=0.2,color=(.7,.7,.7))
plt.title(' Intereference+diffraction, 2 slits 30 $\mu$m wide, 0.24 mm apart')
plt.xlabel('y [cm]')
plt.ylabel('Intensity')
plt.grid()
plt.show()
input('next plot? ')
   
                 
# find parameters C and Ap by Least Squares
        

plt.scatter(vdata,F_fit/9.81e3,s=9,color=(1,0,0)) 
plt.title('2-param. model of drag vs. speed of jet airliner')
# calculate best speed
# dF/dv = -2C/v**3 + Ap rho v == 0 ==> v_fuel = v_glideslope
# d(F*v)/dv = -C/v**2 + 1.5*Ap*rho*v**2 == 0 ==> v_power = v_T_glide
# d(F/v)/dv = -3C/v**4 +Ap rho/2 ==0 ==> v{min_fuel*time}
v_glidesl = v_fuel =(2*C/Ap)**(1/4)     # in [m/s]
v_T_glide = v_power = (C/Ap)**(1/4) 
v_T_fuel       =    (6*C/Ap)**(1/4) 

