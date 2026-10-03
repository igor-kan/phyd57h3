"""
=====================================
ballistic motion with air/water drag
=====================================
"""
from numpy import sin, cos, sqrt
import numpy as np
import matplotlib.pyplot as plt
#mport matplotlib.animation as animation

#-----------------------------------------------------------------------
# launch one simulation of trajectory
# inputs: a = angle in degrees, k = coefficient of drag, graph = 0 or 1
#-----------------------------------------------------------------------
def launch(a,k,graph):
# initial state
	arad = np.radians(a)
# print ('angle',arad,' rad')
# integrate ODE using leapfrog 
# init conditions
	x = 0.; y = 0.; 	vx = v0*cos(arad); vy = v0*sin(arad)
# print(' starting v:',vx,vy)
# x = x + vx*dt/2;  yx = vy + vx*dt/2  # desync pos. and vel., not needed
# set counters 
	height = 0.;  t = 0.;  n = 0;	x_m = 0.; t_air = 1e10
	color = 'blue' if k == 0. else 'red'
	if a < 80.: color = 'blue'
	if a < 30.: color = 'black'
	if a < 22.: color = 'green'
	gdt = g_dt;   gdt_w = 7./8.*g_dt; R = 0.
# time loop
	while (y >= -10.):
		n = n + 1
		v = sqrt(vx*vx+vy*vy)
		f = k * v
		if(y >= 0.):	
			x_prev = x;		y_prev = y
			R = x;  q = 1.;   v_w = v;  clr = color
		if(y < 5.): q = 0.1			#  q reduces timestep near/in water
		if(y < 0.):					# under water
			clr = 'blue'
			f = f *1000./1.225 
			gdt = gdt_w					 # reduction for buoyancy
			if (f*q > 0.2): print(' fq', f*q, ' !!')  
		vx = (1. - f*q)*vx;	vy = vy - (f*vy + gdt)*q
		x = x + vx*dt*q;		y_prev = y;    y = y + vy*dt*q
		if (y_prev >= 0. and y < 0.): 	# precise landing in water
			p = y_prev/(y_prev-y)
			R = x_prev*(1.-p) +x*p
			t_air = t +p*dt*q
		if height < y: 
			height  = y;	x_m = x    # stops updating on descending path
		if graph: 
#			if (n % 1000 == 0): print("x y",x,y)
			if (n==1 or n % 50 == 0): 	plt.scatter(x,y,c=clr,s=2)
		t = t + dt*q	
	R_w = x - R 
	return R, R_w, height, x_m, t_air, v_w


#==============================================================================
#	main
#==============================================================================
v0 = 710.	   # initial speed [m/s]
r = 0.00792/2  # radius of AK-47 bullet [m] 
m = 0.008      # mass of the bullet [kg]
dt = 0.002     # timestep [s]
Cd = 0.35      # nondim. coeff of drag
rho = 1.225	   # air density [kg/m^3]
g_dt = 9.81*dt #  g*dt = dt * accel. of gravity, [m/s]
K = Cd*(rho/2)*(np.pi*r**2)/m *dt	   # Cd * A/M * rho/2 * dt
print('Ballistics problem k =',K,'  A/M =',np.pi*r*r/m)
plt.figure(figsize=(14.5,7))    


#calculations__________________________________________________________________
# simulate vharacteristic angles

R, R_w, H, x_m, tt, v = launch(89., K, 0)
print ('a=89.5 R ',R,R_w,' H =',H,' x_m/R =',x_m/R, ' tt ', tt, ' v',v)

# simulate throw in air, a = 45 deg 
R, R_w, H, x_m, tt, v = launch(45., K, 1)
print ('a=45., R ',R,R_w,' H =',H,' x_m/R =',x_m/R, ' tt ', tt, ' v',v)

# simulate flat throw in air, a = 20 deg 
R, R_w, H, x_m, tt, v = launch(20., K, 1)
print ('a=20., R ',R,R_w,' H =',H,' x_m/R =',x_m/R, ' tt ', tt, ' v',v)
 
# simulate flat throw in air, a = 5 deg 
R, R_w, H, x_m, tt, v = launch(5., K, 1)
print ('a=5., R ',R,R_w,' H =',H,' x_m/R =',x_m/R, ' tt ', tt, ' v',v)

R, R_w, H, x_m, tt, v = launch(1., K, 0)
print ('a=1.0 R ',R,R_w,' H =',H,' x_m/R =',x_m/R, ' tt ', tt, ' v',v)


# find best angle in air
a_opt = 0.; R_prev = 0.
for angle in np.arange(26.1,27, 0.005):
	R_prev = R; 	a_opt = angle-0.005
	R, R_w, H, x_m, tt, v = launch(angle, K, 0)
	text_w_format = 'a %9.3f, R%12.5f %9.3f, H=%9.3f, xm/R=%9.3f, t=%9.3f'
	print(text_w_format	%(angle,R,R_w,H,x_m/R,tt))
	if R < R_prev: break
R_opt = R_prev
print('the optimum angle in air =',a_opt)
# simulate & plot a throw in air at optimum angle
R, R_w, H, x_m, tt, v = launch(a_opt, K, 1)
print ('R, R_w ',R,R_w,' H =',H,' x_m/R =',x_m/R, ' tt ', tt,' v_w', v)


# plotting 

plt.grid()
text = 'Bullet moving init. 710 m/s in air, falling into water. '
text2 = 'Max range at angle: '+ str(round(a_opt,2))+'\u00b0'
plt.title(text+text2,fontsize=15)
plt.xlabel('X [m]',fontsize=14);	plt.ylabel('Y [m]',fontsize=14)
plt.text(1825,670,'max R = '+str(int(round(R_opt,0)))+' m',color='black',fontsize=12)
plt.text(600,170,'20\u00b0', color='green')
plt.text(600, 70,'5\u00b0', color='green')
plt.text(600,630,'45\u00b0', color='blue')
plt.text(600,350,str(round(a_opt,2))+'\u00b0', color='black',fontsize=11)
plt.savefig('bullet.jpg')
plt.show()


