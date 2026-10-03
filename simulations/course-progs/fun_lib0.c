#define PY_SSIZE_T_CLEAN
#define N 10000
#include <Python.h> 
#include <omp.h>
// compile fun_lib.so:   
// gcc -O2 -fPIC -shared -o fun_lib.so fun_lib.c \
// -I/usr/include/python2.6  -std=c99 
// Python2 version Python.h used
 
int f1(int num) 
{ 	int s;
    if (num <= 0) {
  		s = num*num; // if num is < 1 , return its square
        }
    else s = num*19; 
	return s;
} 


int f2(double *indata, size_t size, double *outdata) 
{ 	int s, i, j;
    if (indata[1] <= 0.) {  // indat[0,1] == indata[1]  
  		s = -99; 
         }
    else { 
        s = floor(indata[1]*19.); 
        }
	indata[1] = -4.;
	for (size_t i = 0; i < size; ++i)
		outdata[i] = indata[i] * 2.;
	return s;
} 

