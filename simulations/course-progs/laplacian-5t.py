
#___________numerical blurring by iterated Laplacian_______________
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter,ImageEnhance   
# Pillow handbook online:
# https://pillow.readthedocs.io/en/3.0x/handbook/tutorial.html
plt.interactive(True)
from skimage import io, color
# I had to install scikit-image (skimage) module via
#% pip3 install scikit-image
from time import time 

'''
    Apply Laplacian operator to an image
    Try skimage = scikit-image, and PIL = Pillow
    Unsharp mask the image. 
'''

def Laplacian_diffusion_step(arr,q,n):
# Perform n Laplacian blurring steps.
#
# Notice that no "newarr" temprary array is declared;
# it is not needed, since array arr is modified only after 
# all calculations on its copies kept by NumPy are done.
# In contrast, pixel-wise method needs the explicit temporary 
# array, otherwise it would overwrite the data in arr needed 
# for computation of next pixels. This routine processes array
# about 80 times (two orders of magnitude) faster than Python
# loops in pixel-wise method.
#
#   save borders
    upp=arr[0,:]; lwr=arr[-1,:]; lft=arr[:,0]; rgt=arr[:,-1]
    for i in range(n):
        arr = q*(np.roll(arr,1,axis=1)+np.roll(arr,-1,axis=1)+ \
            np.roll(arr,1,axis=0)+np.roll(arr,-1,axis=0))+ \
            (1-4*q)*arr
        # restore borders
        arr[0,:]=upp; arr[-1,:]=lwr; arr[:,0]=lft; arr[:,-1]=rgt
    return(arr)


def display(arr,title,clean=0):
    if(clean): plt.cla()
    plt.figure(figsize=(10.5,8.5))  # or: dpi=120
    plt.imshow(pic,cmap='rainbow') 
    plt.title(title)
    plt.axis('off')
    plt.show()
    input(' continue? ')
#

def norm_and_display(arr,title,nsig):
# normalize, truncate
    N = arr.shape[0]; M = arr.shape[1]
    a_m = arr.mean()
    a_s = arr.std()
    lev_0 = a_m - nsig*a_s
    lev_1 = a_m + nsig*a_s  
    np.clip(arr,lev_0,lev_1)
    arr = (arr-lev_0)/(lev_1-lev_0)
    plt.figure(dpi=120)  #(figsize=(6,6))
    plt.imshow(arr, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

    
#--------Main program--------------------------------------------

# use scikit-image (skimage)
# pictures read/written in local directory
t0 = time()
#pic = io.imread('M81.jpg')
pic = pic0c = io.imread('M81.jpg')
t1 = time() - t0
# this demonstrates the type of data read from the file
print('pic pic[80,90]',type(pic),type(pic[80,90]),pic[80,90])
#print('R R[80,90]',type(R),type(R[80,90]),R[80,90])
# turn into grayscale float np.array
pic = pic0 = color.rgb2gray(pic)
# this proves a conversion was done to float64 array 
print('pic pic[80,90]',type(pic),type(pic[80,90]),pic[80,90])
#
t2 = time() - t0
print(' t1, t2  %7.4f %7.4f ' %(t1,t2))
#
plt.figure(dpi=220)  #(figsize=(6,6))
plt.imshow(pic, cmap='gray')
plt.axis('off')
plt.show()
input(' blur? ')
#
# iterate Laplacian-based steps  
q = 1/5
N = pic.shape[0]
M = pic.shape[1]
print('N,M',N,M)  
# notice N<M, i.e. pic[vertical pos.,horiz.pos.]
mode = 'numpy vectorized' # or 'loop'
N_blur = 1200
n_blur = N_blur//10
if(mode=='loop'):
    N_blur = n_blur = 30
    newpic = np.empty_like(pic) 
t00 = time()
for iter in range(n_blur):  # n_blur = 1200/10
    t0 = time()

    
    if (mode=='loop'):   # slow method, Turner et al book p.46
        iteration = iter
        p4 = 1 - 4*q        # if q=1/5 then p4=1/5 too
# pixel-wise processing, fairly slow. curiously, there appear
# to exist even slower methods (putpixel, getpixel)
        for i in range(1,N-1):
            for j in range(1,M-1):
                newpic[i,j] = q*(pic[i+1,j]+pic[i,j+1]+
                    pic[i,j-1]+pic[i-1,j]) +p4*pic[i,j]
        # borders are garbage, exclude from update
        pic[1:-1,1:-1] = newpic[1:-1,1:-1]

    else:                # numpy-vectorized processing mode  
        iteration = iter*10
        pic = Laplacian_diffusion_step(pic,q,10)
# Laplace step done, do not normalize
    t3 = time() - t0
    if(iter%20==0): 
        print(iteration,' t(Lapl)=',t3,'  pic[80,90]',pic[80,90])
t1 = (time() - t00)/(10*n_blur)
t1m = t1*1024*1024/(N*M)
print('time per one pass ',np.around(t1,6), np.around(1./t1,6))
print('time 1M pixels    ',np.around(t1m,6),np.around(1./t1m,6))
# all iterations done, write blurred image
io.imsave('M81-blur.jpg',pic)

# unsharp masking
enh = pic0 - pic
a_m = enh.mean();     a_s = enh.std()
a_mx = enh.max();     a_mn = enh.min()
lev_0 = a_m -0.1*a_s;   lev_1 = a_m +0.2*a_s
print('min and max of arr %7.4f %7.4f' %(a_mn,a_mx))
print('mean, std %7.4f %7.4f L0/1 %7.4f %7.4f' %(a_m,a_s,lev_0,lev_1))
# numpy.clip(a, a_min, a_max) replaces outliers with limits
# could also be accomplished (slower) by np.minimum(a, a_min) etc.
np.clip(enh,lev_0,lev_1)
# bring values in enhanced array enh into the 0..1 range 
enh = (enh - lev_0)/(lev_1 - lev_0)      
# save
io.imsave('M81-unsh.jpg',enh, cmap='rainbow')
#
title='M81 after N='+str(N_blur)+' Laplace iter. q='+str(q)
display(enh,title,clean=0)

title='M81 after unsharp masking. q='+str(q)+', N = '+str(N)
plt.figure(figsize=(7.5,6.5))
plt.imshow(enh, cmap='rainbow')
plt.axis('off')
plt.show()
    
