// example of dislin graphics, compile and run on art-2 in your subdir.
// compilation:
// 	icc -O2 ex11_1.c -o ex11_1.c.x -I/usr/local/dislin -ldislin
#include <stdio.h>
#include <math.h>
#include "dislin.h"
#define N 256

float map[N][N];

int main ()
{ int n = N, i, j;
  double  fpi = atan(1.)*4./180.0, dx, x, y;

  dx = 360.0 / (n - 1);
  for (i = 0; i < n; i++)
  { x = i * dx;
    for (j = 0; j < n; j++)
    { y = j * dx;
      map[i][j] = (float) (2. * sin(fpi*x) * sin(fpi*y));
    }
  }

  scrmod ("revers");
  metafl ("cons");
  disini ();
  pagera ();
  hwfont ();

  titlin ("3-D Colour Plot of the Function", 2);
  titlin ("F(X,Y) = 2 * SIN(X) * SIN(Y)", 4);

  name   ("X-axis", "x");
  name   ("Y-axis", "y");
  name   ("Z-axis", "z");

  intax  ();
  autres (n, n);
  axspos (300, 1850);
  ax3len (2200, 1400, 1400);

  graf3  (0.0, 360.0, 0.0, 90.0, 0.0, 360.0, 0.0, 90.0,
            -2.0, 2.0, -2.0, 1.0);
  crvmat ((float *) map, n, n, 1, 1);
  
  height (50);
  title  ();
  disfin ();
  return 0;
}
