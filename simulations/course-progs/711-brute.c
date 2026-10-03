#include <stdio.h>
/* Brute force search for solutions to 711 puzzle
 x+y+z+r = 711,
 x*y*z*(711-x-y-z) = 711*10**6  
 All prices are in cents.
 All combinations such that x <= y <= z  are generated
 but only if  x <= y <= z <= r the equation is checked. */

 int main() {	
   int  n,m, x,y,z,r; 
   n = 0;
   for (x=1; x < 709; x++) {
	for (y = x; y < 710-x; y++) {
	 m = 711-x-y;
	 for (z = y; z < m; z++) {
	  r = m-z;
	  if (r > z) {
	  n++;				// count & check equation
	  if (x*y*z*r==711000000)   
		 printf(" prices: %d %d %d %d cents\n",x,y,z,r);
	  }
	 }
    }
   }
   printf(" checked %d cases \n",n); 
}
