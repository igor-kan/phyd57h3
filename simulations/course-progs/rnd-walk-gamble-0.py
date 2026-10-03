'''
    Gambler simulations: starts at N = N0 and puts $1 on red in 
    a fair roulette (not at a casino!) or throws a fair coin.
    Watch the gambler lose or win for M steps, where sqrt(M) > N0, 
    and break simulation if the gambler is ruined. 
    Overplot many simulations and an envelope y = N0 +- sqrt(t).
    N(t) is the current capital.   
'''
import numpy as np 
import matplotlib.pyplot as plt
plt.interactive(True)

#   initial number of $$ is N0 
N = N0 = int(input(" initial capital, N0 = "))  # notice double '='
# steps of the gamble
M = 4 * N0**2     
# use fair coin
P = 0.5
# this is overall gain for all the games played
gain = 0
#   prepare plot frame and description
plt.figure(figsize=(10,6.6))
plt.xlabel('t [K]',fontsize=14)
plt.ylabel('N',fontsize=14)
plt.title('Gamblers capital starting from N$_0$='+
          str(N0),fontsize=14)
plt.grid(True,color=(.8,.8,.9))
# prepare the theoretical envelope functions
tt = np.linspace(0,M-1,M)
env = np.sqrt(tt)
lower_env = N0-env
looow_env = N0-2*env

# Main time loop. Compute and plot N(t)/N0
ruins = 0
for i in range(100):   
    t = 0;      N = N0
    capital = np.zeros(M)     # store results here
    capital[0] = N0
# precompute all M outcomes of coin throws 
    win = (np.random.random(M) < P) # array; True if rnd# < P
    while (t < M-1 ):
        t += 1
        if (win[t]):
            N += 1   # if win[t] is True, add $1
        else:        # subtract $1
            N -= 1
        # You can print each simulation for debugging
        # print('at time t=',t,' win=',win[t],' N=',N
        capital[t] = N          # store capital at time t
# end of a game
    gain = gain +(N-N0)
    if (N==0): 
        ruins += 1
        plt.scatter(t/1000,0.,s=11,color=(1,0,0))
# output
    t_k = tt/1000
    plt.plot(t_k,capital,color=(0,0,1),linewidth=0.7,alpha=0.4)
    plt.plot(t_k,capital,linewidth=1)
    plt.plot(t_k, N0 + env,linewidth=1,color=(.3,.3,.3),alpha=0.5) # upper envelope
    plt.plot(t_k, N0+2*env,linewidth=1,color=(.3,.3,.3),alpha=0.5) # upper envelope
    plt.plot(t_k,lower_env,linewidth=1,color=(.3,.3,.3),alpha=0.5) # lower envelope
    plt.plot(t_k,looow_env,linewidth=1,color=(.3,.3,.3),alpha=0.5) # lower envelope
    plt.show()
    print(i+1,'runs, %ruin =',np.around(ruins/(i+1),4),
        ', gain = $',gain)
    ans = input(" one more run ? ")