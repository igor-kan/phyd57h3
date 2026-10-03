# use C functions from Python2 [or Python3 if you change print  to print( )]
import numpy as np, ctypes as ct
from  numpy.ctypeslib import ndpointer  
so_file = './fun_lib.so'
my_fun = ct.CDLL(so_file)

# first way of calling a C function, single int argument and result
# so no type conversion needed
#print ' type of my_fun: ',type(my_fun))
print ' my_fun.f1(-5) ',my_fun.f1(-5)
print ' my_fun.f1( 5) ',my_fun.f1( 5)

# more complicated argument passing by reference not value
fun2 = my_fun.f2
fun2.restype = int
fun2.argtypes = [ndpointer(ct.c_double, flags="C_CONTIGUOUS"), 
	ct.c_size_t, ndpointer(ct.c_double, flags="C_CONTIGUOUS")]

# pass and receive numpy arrays by reference
indat  = np.ones ((3,4))
outdat = np.empty((3,4))
istatus = fun2(indat, indat.size, outdat)
print ' fun2 returns  ',istatus
print ' indat \n',indat,'\n outdat \n',outdat

''' 
output:
 my_fun.f1(-5)  25
 my_fun.f1( 5)  95
 fun2 returns   19
 indat 
[[ 1. -4.  1.  1.]
 [ 1.  1.  1.  1.]
 [ 1.  1.  1.  1.]] 
 outdat 
[[ 2. -8.  2.  2.]
 [ 2.  2.  2.  2.]
 [ 2.  2.  2.  2.]]

'''
