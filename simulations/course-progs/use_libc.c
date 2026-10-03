#define N 120000000
#define I 10
#include <omp.h>
#include <stdio.h>
#include <math.h>
// compile use_libc.c   
// gcc -fPIC -O2 -fopenmp use_libc.c -std=c99 -o use_libc.x  -L. -lfun

 extern void f2 (void);

 int main() {
 	int istatus, i, j;
	f2 ();
 	return 0;
} 

