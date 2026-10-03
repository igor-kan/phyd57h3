# epi-4.py
# spatio-temporal simulation of epidemic 

import numpy as np, tkinter as tkr, random as rnd, time 

WIDTH = 1000; HEIGHT = 700
N = 800;     R = 10;    Rint = 2*R
tau_lat   = 0.5  # wks
tau_sympt = 3.5  # wks
tau_contg = 9/7 # wks 
colors = ["white","orange","red","light green"]

# Create canvas
tk = tkr.Tk()
canvas = tkr.Canvas(tk, width=WIDTH,height=HEIGHT)
tk.title("Outbreak")
canvas.pack()
#canvas.grid()



class Person: 
    def __init__(self, color, x, y, vx, vy):
        self.shape = canvas.create_oval(x,y,x+R,y+R,fill=color)
        self.xspeed = vx;  self.yspeed = vy

        
    def move_n_infect(self): 
        canvas.move(self.shape, self.xspeed, self.yspeed)
        pos = canvas.coords(self.shape)
# randomize speeds every 4th step but not all simultaneously
        if((i+step)%4 == 0):
            self.xspeed = rnd.randrange(-60,61)/10.  # -6 to +6
            self.yspeed = rnd.randrange(-60,61)/10.
        if (status[i]>0): 
            canvas.itemconfig(self.shape, fill=colors[status[i]])
            if(status[i]==2): # symptomatics move slowly 
                self.xspeed = rnd.randrange(-2,3)
                self.yspeed = rnd.randrange(-2,3)
# store data
        pers_data[i,1] = self.xspeed
        pers_data[i,2] = self.yspeed
        pers_data[i,3] = (pos[0]+pos[2])*0.5  # x 
        pers_data[i,4] = (pos[1]+pos[3])*0.5  # y
# progress of individual illness
        if(status[i] > 0):      # SARS-CoV-2 (+)
            pers_data[i,5] += dt   # clock time since infection [wk]
            if(pers_data[i,5] > tau_lat): # i has symptoms after latent period
                status[i] = 2
            if(pers_data[i,5] > tau_sympt): # resolved after tau_sympt
                status[i] = 3
        
# enforce periodic boundaries
        if pos[3] >= HEIGHT:  canvas.move(self.shape,0,-HEIGHT)
        if pos[1] <= 0:       canvas.move(self.shape,0,+HEIGHT)
        if pos[2] >= WIDTH:   canvas.move(self.shape,-WIDTH,0)
        if pos[2] <= 0:       canvas.move(self.shape,+WIDTH,0)  
# infection event during tau_contg
        if(status[i] > 0 and pers_data[i,5] <= tau_contg):  # contageous i
            dist_x = abs(pers_data[0:N-1,3]-pers_data[i,3]); dist_x[i] = WIDTH
            dist_y = abs(pers_data[0:N-1,4]-pers_data[i,4]) 
            p_infect = 1. - ((dist_x+dist_y)/Rint)   
        # i infects the nearest j with probability p_infect
            j = np.argmax(p_infect)   # closest neighbor  
            if (rnd.random() < p_infect[j] and status[j]==0): 
                status[j] = 1 
                pers_data[i,6] += 1.  # count of infected by person i
                pers_data[i,7] = t
                

                
#_____________
# main program
#_____________
# SIR model of pandemic spread, latent period 0.5 wks, symptomatic 3.5 wks
people = []
pers_data = np.zeros(shape=(N,8))
z = np.zeros(N)
status = np.zeros(N,dtype=np.uint8)  # everybody is initially susceptible
# generate N susceptible persons
for i in range(N):
    x  = rnd.randrange(R,WIDTH-R);   y = rnd.randrange(R,HEIGHT-R)
    vx = rnd.randrange(-60,61)/10.; vy = rnd.randrange(-60,61)/10.
    people.append(Person("white",x,y,vx,vy))
status[0] = 1  # patient 0 infected & asymptomatic (2=symptomatic, 3=resolved)

T_end = 30  # time measures in weeks 
t = 0;  step = -1;  dt = 1/7/4

history = np.zeros(shape=(int(T_end/dt+1),8))
asy = 1 ; sym = 0
# main time loop
while (t < T_end and asy+sym > 0):
    dn,ifcd,asy,sym,rcvd,R0 = 0,1,0,0,0,1
    tim0 = time.time()
    step += 1
    t += dt 
    dn = 0
    for i in range(N):
        person = people[i]
        person.move_n_infect()
    
    tim1 = time.time() - tim0;  delta = 0.03-tim1 
    ctg = 0; non = 0;  numi = 0; infd = 0; symptom = 0
    
    for i in range(N):
        if(status[i]==0): non += 1
        if(status[i]==1): asy += 1
        if(status[i]==2): sym += 1
        if(status[i]==3): rcvd += 1
        if(pers_data[i,5]<tau_contg): ctg += 1
        if(pers_data[i,6] > 0): 
            infd += pers_data[i,6]; numi += 1; R0 = infd/numi
    
    prev_symptom = symptom    
    symptom = N-non
    frac_asy = asy/(1e-10+symptom)
    tk.update()
    if(delta > 0.):  
        time.sleep(delta)
    history[step,0:6] = t,non,asy,sym,ctg,rcvd
    
    if(step>0): prev_symptom = history[step-1,3]
    if(step>0): history[step,7] = symptom - prev_symptom
    
    print(step,' t',np.around(tim1,3),' dn,asy+sym,rcvd', \
      history[step,7],sym, rcvd, ' %asy,R0 ',frac_asy,np.around(R0,3))
   
tk.mainloop()

import matplotlib.pyplot as plt
#plt.plot(history[0:step,0],history[0:step,3],color=(.7,.7,.9),alpha=0.4)
plt.plot(history[0:step,0],history[0:step,7],color=(.7,.7,.9),alpha=0.4)

plt.show()
