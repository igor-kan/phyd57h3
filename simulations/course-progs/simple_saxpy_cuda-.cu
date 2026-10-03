#include <stdio.h>
#include <omp.h>

void saxpy(int n, float a, float *x, float *y)
{
#pragma omp parallel for num_threads(6)
  for (int i=0; i<n; i++)   y[i] = a*x[i] + y[i];
}

int main(void)
{
  float *x, *y;	     int N = 1<<30;      // N = 1G = 2**30 
 // allocate 8 GB on heap in CPU RAM
  x = (float*)malloc(sizeof(float)*N);  y = (float*)malloc(sizeof(float)*N); 
  for (int i = 0; i < N; i++) {x[i] = 1.0f;  y[i] = 2.0f;} // init x,y
  
  double t0 = omp_get_wtime();
 // Perform SAXPY on N elements of 2 arrays on CPU 
  saxpy(N, 2.0f, x, y);

  double t =  omp_get_wtime() - t0; 
  float GBytes = 3*(1e-9* 4*N);  // total transferred
  printf("\n This program is bandwidth-limited (CPU-RAM) \n");
  printf(" %f GB transferred in %fs, bandwidth %f GB/s\n",GBytes,t,GBytes/t);
	
  float maxError = 0.0f; for (int i = 0; i < N; i++)
    	maxError = max(maxError, abs(y[i]-4.0f));
  printf("Max error: %f\n", maxError);
  free(x);  free(y);  // free CPU memory
}
