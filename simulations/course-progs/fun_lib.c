#define PY_SSIZE_T_CLEAN
#define N 120000000
#define I 10
#include <Python.h> 
#include <omp.h>
// compile fun_lib.so:   
// gcc -O2 -fopenmp -fPIC -shared -o fun_lib.so fun_lib.c \
// -I/usr/include/python2.6  -std=c99 
// Python2 version Python.h used

float arr[N];

int f1(int num) 
{ 	int s;
    if (num <= 0) {
  		s = num*num; // if num is < 1 , return its square
        }
    else s = num*19; 
	return s;
} 


int f2(double *indata, size_t size, double *outdata) 
{ 	int s, i, j, k;
	float t;
	double t0, t1;
    if (indata[1] <= 0.) {  // indat[0,1] == indata[1]  
  		s = -99; 
         }
    else { 
        s = floor(indata[1]*19.); 
        }
	indata[1] = -4.;
	for (size_t i = 0; i < size; ++i)
		outdata[i] = indata[i] * 2.;


// test of omp multithreading 	
	t0 = omp_get_wtime();
#pragma omp parallel for num_threads(12) schedule(static,10000000) 
	for (i=j=0; i<N; i++) {
	  arr[i] = 1.2345*i+1.*j;
	  for (k=0; k < I-1; k++) arr[i] = 2*arr[i]-0.1+i;
	 // if (j < 0 && omp_get_thread_num() == 0) {
	 //	j++; printf("%d ",i);
	 // } 
	}
	t = (float)(omp_get_wtime() - t0);
	printf ("\n arr[100]= %f  t=%f\n", arr[100],t);
	printf ("bandw = %f GB/s;  eqiv GFLOPS= %f\n",N*I*4e-9/t,N*I*3e-9/t);
	return s;
} 

