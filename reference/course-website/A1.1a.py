# non-circular, somewhat squareish loop model
# r = R(1+q sin(2 fi))
q = 0.0 		# 0.06 <-> v0=178 m/s, Cd=0.1
#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
pi = np.pi
# assume drag coeff. at n=1 is C=0.1; A=28 m^2, v0 = 180 m/s = 350 kt.
R = R0 = 660 	# m,     3.28084 ft = 1m 
v0 = v = 180				# m/s
M = 15e3 					# kg
Cd0 = 0.1;   rho_air = 1.22;	 	A = 28. #  units: 1; kg/m^3;  m^2
D0 = Cd0 * A * rho_air * v0**2 /2 /M  		# N/kg
T0 = T = 9.5e3*9.81/M    # specific thrust [N/kg], assume thrust 98.1 kN = 10t
fi = 0.
dfi0 = dfi = v/R
g = 9.81  # m/s^2
dt = 0.001

print(f"R= {R:.2f} v0 = {v0:.3f} D0 {D0:.3f}  T-D {T0-D0:.3f}")
N = int(36/dt)
M = N//50
traj = np.zeros((9,M))   # dtype=np.float64 by default. data for plotting

for i in range(N):
	s  = np.sin(fi);		c  = np.cos(fi)
	s2 = 2.*s*c 		# sin(2*fi)
	s4 = np.sin(4*fi); 		c4 = np.cos(4*fi)
	r = R*(1.+q*s2*s2);		r_2 = r*r
	dr_dfi = 2*R*q*s4  				# dr/dfi
	dr_dfi_2 = dr_dfi * dr_dfi 		# r'^2 = (dr/dphi)^2
	d2r_dfi2 = 8*R*q*c4        		# r" = d2r/dfi2
	ds_dfi = np.sqrt(r_2 + dr_dfi_2)	# dS/dfi
#  k = curvature = 1/Rc = inverse radius of curvature
	numerator = 2*dr_dfi_2 -r*d2r_dfi2 +r_2 
	k = numerator/ds_dfi**3     #  numer/(dr_dfi_2 +r_2)**1.5
#	v = (ds/dfi)*(dfi/dt)  is the speed along trajectory
#   dv/dt = d^2S/dt^2 = sum of accelerations along the trajectory
#   n_cent is equal v^2/Rc = k*v*v indep. of posit. of center of curvature
	n_perp = k*v*v/g + c   # assumes Rc begins at loop's center (good approx) 
#  taking into account that n=6 involves doubling of total drag coeff  
	acc = -g*s -(4+n_perp)/5*D0*(v/v0)**2 + T	 # accel. along traj.
	v = v + dt*acc
#  ds = v dt = dfi * (ds/dfi) 
	dfi = v*dt/ ds_dfi 
	fi  = fi + dfi
	v_kt = v *3.6/1.852		# airspeed [kt] 
	vS = 110*np.abs(n_perp)**0.5
	h = R - c*r				# AGL [m]
	if(i%100==0): 
		phi = fi*180/pi;		a = acc/g
		print(f"{(i//50):} {i*dt:.4f}s {h:.1f}m, v[m/s,kt] {v:.2f} {v_kt:.2f} \
   n {n_perp:.3f} , a {a:.4f}, r = {r:.1f} rc/r {1/k/r:.3f}  {phi:.2f} deg") 
	if(np.abs(fi-pi) < 0.0002): 	print("^^^ top: ",h,v,v_kt,n_perp)
	if(np.abs(fi-pi*1.5) < 0.0002): print("vertic : ",i*dt,h,v,v_kt,n_perp)
	if(v_kt < vS): print('STALL! ',i*dt,h,v_kt,vS)
	if(v_kt < 1.1*vS): print('1.1*vS',i*dt,h,v_kt,1.1*vS)
	if(v_kt < 110*(1.1*np.abs(n_perp))**.5): print('1.1n STALL',i*dt,h,v,v_kt)
# store data for analysis every 50 ms 
	if(i%50==0): 
			traj[:,i//50] = [dt*i, r, fi, v, v_kt, 1/k, n_perp, acc/g, vS]
	if(fi > 2*pi): break
	
print(f"end t={i*dt:.4f} v[m/s,kt] {v:.4f} {v_kt:.4f} n {n_perp:.3f}\
 vS[kt] {110*n_perp**.5:.3f}")
e = i//50 -1 
 # plot
fig, ax = plt.subplots(figsize=(10,10.5))
fig.subplots_adjust(top=0.87)

print("plot has",e," points")
tim = traj[0,0:e]
rad = traj[1,0:e] 
ang = traj[2,0:e]
#rc_r= traj[5,0:N//25-1]/rad
n   = traj[6,0:e]
a   = traj[7,0:e]
v   = traj[3,0:e]  # m/s
vs  = traj[8,0:e]  # kt
x   =       rad * np.sin(ang)
y   =  30+R0 -rad*np.cos(ang)
xt  =    rad[0:e:20] * np.sin(ang[0:e:20])      # special points every second
yt  =  30+R0 -rad[0:e:20] * np.cos(ang[0:e:20]) # special points every second
xi  =    0.78*rad[0:e:20] * np.sin(ang[0:e:20])      # inner point every sec
yi  =  30+R0 -0.78*rad[0:e:20] * np.cos(ang[0:e:20]) # inner point every sec
ycir = 30+R0*(1 - np.cos(ang))
plt.plot(x,ycir,'g')    # green circle
plt.plot(x,y,'b')       # blue trajectory 
plt.plot(x,30+y*0,'b')  # blue trajectory (horiz.)
plt.plot(x,y*0,'r.')	# red ground level
plt.plot([-10,+10],[30+R0,30+R0],'r');  plt.plot([0,0],[20+R0,40+R0],'r')
# annotate
plt.plot(xt,yt,'k.')	# points marked on the curve
nt = n[0:e:20];   vt = v[0:e:20]*3.6/1.852;  vst = vs[0:e:20]
for t in range(27): 
	dx = 13;  dy = 17
	if(t==1): dx = -3
	if(t==1): dy += 16
	if(t==2): dy = -23
	if(t==3): dx += 15
	if(t==3): dy -= 15
	if(t==4): dx += 17
	if(t==17): dy += 13
	if(t==18): dy += 30
	if(t==19): dx = 3
	if(t==19): dy += 30
	if(t==20): dx += 24
	if(t==20): dy = 4
	nf = f"{nt[t]:.2f}"
	ax.text(dx+xt[t],dy+yt[t],nf,fontsize=11)
	vf = f"{vt[t]:.0f}"   
	ax.text(xi[t],yi[t],vf,color='blue',fontsize=10)
	vsf = f"{vst[t]:.0f}"
	ax.text(xi[t],yi[t]-33,vsf,color='orange',fontsize=10)
	fig.suptitle("F-16 loop of the blue shape\
 $r(\phi) = R_0 (1 + q \,\sin^2 2\phi)$", fontsize=13) 
	ax.set_title("$R_q=$ 660 m;  q=0;  Thrust T=9.5 ton = const.\
  Entry speed 350 kt.  Loop time 26.5 s.")
	ax.set_xlabel('X [m]'); 	ax.set_ylabel('Altitude AGL [m]')
# hatch the ground
for i in range(30):
	x = -R0 +2*R0*i/29.5
	plt.plot([x,x+22],[0,-40],'r') 
plt.show()

