# Python code for Mandelbrot Fractal 

# Import necessary libraries 
from PIL import Image 
from numpy import complex, array 
import colorsys 
import numpy as np

# setting the width of the output image as 1024 
Wx = 640;   Wy = 640;   Wy05 = Wy//2

# function defining mandelbrot fractal
def arty(x, y, res):
    z = complex(x,y)
    res[0] = z
    c = z
    for i in range(1,128): 
        if (c.real**2+c.imag**2 > 64.):            
            return (i, 200-i//2,i*2)
        c = z**c
        res[i] = c
    # check some periodicities if not diverged
    for period in range(1,100):
            delta = c - res[i-period]
            if (abs(delta) < 0.02): 
                q = period*4  # 1..255 
                return (255-period, int(255*(period/256)**2), 40+period)
    return (0, 0, 0) 

''' Exponential fractal '''
    
xscale = 0.1;   yscale = xscale
print(" scale factor", xscale)

# creating the new image in RGB mode 
img = Image.new('RGB', (Wx, Wy) ) 
#pixels = img.load() 
res = np.empty(256,dtype=complex)

for x in range(Wx): 
    # displaying the progress at every n-th column
    if (x//100*100==x): print("#"*(x//100)) #print("%.2f %%" %(x/Wx*100.))
    xx = (2*x/Wx -1)*xscale
    for y in range(Wy05): 
        triplet = arty(xx, yscale*y/Wy05, res) 
        #pixels[x,Wy05+y]   = tri
        #pixels[x,Wy05-y-1] = tri
        img.putpixel( (x,Wy05+y)  ,triplet)
        img.putpixel( (x,Wy05-y-1),triplet)
# display the fractal 
img.show() 
