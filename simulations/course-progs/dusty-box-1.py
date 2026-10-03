'''
    dusty-box.py
    
    What is the fraction of radiation remaining in original 
    beam of unit flux that passes through opaque medium filled with 
    small absorbing particles (of assumed cubic shape),
    whose combined area is equal to the side area of a cubic box in which they are randomly positioned?
    
    Divide side area of the box into N x N = 800x800 pixels, consider
    M=3*(N/S)^2 particles, each of diameter S: SxS pixel square.
    
    Radiation transfer equation gives this theoretical answer:
        I = I0 *exp(-tau(x)), where I0 is the initial flux, and
        tau = integral (total) cross secional area of all particles betwen
         positions 0 and x.
    In our case tau = 1, I0 = 1, so for instance at tau=1 
    we should theoretically get flux 
        I = exp(-1) = 1/2.718...
    Compare this with numerics. Overplot num. results for about 32 different 
    M's on the graph of the theoretical I(x) dependance.
'''

def projection (S,N,m1,m2,x,y,box):
#  this function projects dust particles m1:m2 onto a screen (box) 
#  ea. point is a square SxS pixels (S assumed even)
    s = S//2
    for i in range(m1,m2):  # particles m1,...,m2-1
        ix = int(x[i]*N)
        iy = int(y[i]*N)
        box[ max(ix-s,0):min(ix+s,N-1), max(iy-s,0):min(iy+s,N-1) ] = 1

#__________________________________________________________________________      
# main program
import numpy as np
import matplotlib.pyplot as plt
plt.interactive(True)

S = 8                 # dust grain diameter
N = 800               # image will be NxN pixels
M = int(3*N*N/(S*S))  # largest number of particles considered (->tau=3)
print('M=',M,' particles in a square grid of size',N,'x',N)
x = np.random.random(M)  # x coordinates of particles
y = np.random.random(M)  # y coordinates of particles
box = np.zeros((N,N),dtype=np.int8)  # initially empty box
# start plotting
plt.figure(figsize=(7.4,7.4))
n = plt.scatter(x,y,s=5,alpha=0.5)
plt.title('positions of particles projected on the screen')
plt.grid(True)
plt.show()
ans = input("fill array?")


# divide the particles into K batches and fill the array stepwise 
K = 32
res = np.zeros((4,K+1),dtype=float)   # storege for results
res[1,0] = 1.

for j in range(K):
    m1 = j*(M//K)   
    m2 = m1 + M//K
#    print("filling box with particles from",m1," to almost ",m2)
    projection(S,N,m1,m2,x,y,box)
    count_1s = box.sum()
    count_all= N*N
    count_0s = count_all - count_1s
    tau = S*S*m2/(N*N)
    I_theor = np.exp(-tau)   # radiation transport equation predicts this
    equiv0_p = count_0s/(S*S)
#   print('1s,0s', count_1s,count_0s,'  np_0^-.5 =',
#          np.around(equiv0_p**(-0.5),4))
    I = count_0s/count_all                  # flux(tau)
    sigma = I*equiv0_p**(-0.5)
   # 
    print('layer',j,'tau',tau,'I =',
          np.around(I,4),'+-',np.around(sigma,4),' vs.',
          np.around(I_theor,4),'+',np.around(I-I_theor,4))
# store
    res[0,j+1] = tau
    res[1,j+1] = I
    res[2,j+1] = sigma
# plot 
    n = plt.imshow(box)
    plt.grid(True)
    plt.show()
    if(j%4==0): 
        ans = input("next?")


ans = input("final plot?")

plt.figure(figsize=(8.5,6.0))
x = np.linspace(0,3.,300)
plt.plot(x,np.exp(-x))
n = plt.scatter(res[0,:],res[1,:],s=12,linewidth=2,alpha=0.75,color=(1,.4,.4))
plt.title('Transmitted flux, theoretical (line) and numerical (points)')
plt.xlabel('optical thickness')
plt.ylabel('I(x)')
plt.grid(True)
plt.show()

ans = input("finalize?")


