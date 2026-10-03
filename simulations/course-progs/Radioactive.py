'''
    Radioactive decay simulation using pseudorandom numbers.
    
    Uranium U-235 (natural radioactive isotope) decays like so
    
    U-235 --[half-life=703.8 Myr]---> Th-231 + He-4 + 2n --> ... --> 
                                 -->   Pb-207 (stable)
    
    [This is a spontaneous decay, different from the chain reaction 
    induced by neutrons in reactors and nuclear bombs,
    U-235 + n --> U=236 -->  Kr-92 + Ba-141  +3n.]
    
    Let's call the initial number of uranium atoms U0, Try different U0's. 
    Plot the evolution of that amount of Uranium 235, U(t),
    for 4.5 Gyr or the age of Earth. Overplot theoretical exp(-t*c) curve.
    Divide time in intervals of dt = 0.01 Gyr, and for every nucleus
    with with probability P = dt*lambda remove it from the shrinking 
    pool of uranium and add to the growing pool of stable lead nuclei.
    lambda is straightforwardly related to half-life, which we denote as t12.
    U = -U*lambda*dt  ==> U = U0 exp(-lambda*t), while in half-life notation
    U = U0 (1/2)**(t/t12)
    Comparing natural logarithms of these eqs., we get: 
    lambda = ln(2)/t12. 
    Use P = dt*lambda = ln(2)*dt/t12 in every time step U times, and 
    watch the number U shrink in time
'''
import numpy as np 
import matplotlib.pyplot as plt
plt.interactive(True)

#   initial number of nuclei is U0 
U = U0 = int(input(" initial # of nuclei = "))  # notice double '='
t12 = 0.7038   # [Gyr]
dt  = 0.01     # [Gyr]
# calculate probability P that a given nucleus decays in time dt
P = np.log(2)*dt/t12   # decay probability per timestep per nucleus
lambd = np.log(2)/t12  # rate constant of decay
#   prepare plot frame and description
plt.figure(figsize=(8,6.4))
plt.xlabel('t [Gyr]',fontsize=14)
plt.ylabel('U/U$_0$',fontsize=14)
plt.title('Radioactive decay of U-235',fontsize=14)
plt.grid(True,color=(.9,.9,.97))
plt.text(.3,.98,'U$_0$ = '+str(U0)+' nuclei',fontsize=14)
# prepare the theoretical exponential decay function
tt = np.linspace(0.,4.5,600)
theor = np.exp(-lambd*tt)

# Main time loop. Compute and plot U(t)/U0, as well as Pb/U ratio
while True:     # to break out of infinite loop, CTRL-D when asked 
    U = U0;   Pb = 0;   t = 0
    while (t < 4.5 and U > 0):
        t = t + dt
        U_previous = U
# give a chance to decay to all U nuclei: genrate U rnd numbers
        ran = np.random.random(U)
# if random numer from 0 to 1 is less than P, set decay to True
        decay = ran < P         # array of Boolean True/False values,
        N_decays = decay.sum()  # which can be summed (True=1, False=0) 
        U = U - N_decays
        # You can print each simulation, good for debugging!
        # Pb = U0 - U             # all U's decay to Pb's, so Pb+U==U0
        # print('at time t=',np.around(t,4),' U=',np.around(U,4),
        #  ' Pb/U=',np.around(Pb/U,3)) 
# plot 1 time segment of the decay curve 
        plt.plot([t-dt,t],[U_previous/U0,U/U0],color=(0,0,1),linewidth=2)
    
    plt.plot(tt,theor,linewidth=1.5,color=(1,0,0)) # overplot exp(-lambd*tt)
    plt.show()
    ans = input(" one more? ")