# Python code for Mandelbrot Fractal 

# Import necessary libraries 
from PIL import Image 
from numpy import complex, array 
import colorsys 

# setting the width of the output image as 1024 
Wx = 600;   Wy = 600;   Wy05 = Wy//2

# function defining mandelbrot fractal
def arty(x, y):
    z = complex(x,y)
    c = z
    for i in range(1,256): 
        if (c.real**2+c.imag**2 > 4): 
            return (i//2,200-i//2,i)
        c = z**c
    return (0, 0, 0) 

''' Exponential fractal '''
    
xscale = 0.1;   yscale = xscale

# creating the new image in RGB mode 
img = Image.new('RGB', (Wx, Wy) ) 
#pixels = img.load() 

for x in range(Wx): 
    # displaying the progress at every n-th column
    if (x//100*100==x): print("#"*(x//100)) #print("%.2f %%" %(x/Wx*100.))
    xx = (2*x/Wx -1)*xscale
    for y in range(Wy05): 
        triplet = arty(xx, yscale*y/Wy05) 
        #pixels[x,Wy05+y]   = tri
        #pixels[x,Wy05-y-1] = tri
        img.putpixel( (x,Wy05+y),triplet)
        img.putpixel( (x,Wy05-y-1),triplet)
# display the fractal 
img.show() 
