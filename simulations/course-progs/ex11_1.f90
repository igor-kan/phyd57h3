! example of dislin graphics, compiles with ifort  (full options below not 
!  necessary..)
! compile and run on art-2 in your subdir.
!  ifort -qopenmp -O3 -no-prec-div -fp-model fast=2 -xHost -L$DISLIN10 -ldislin10 -I$DISLIN10/ifc -L/opt/intel/composer_xe_2015.3.187/compiler/lib/intel64 -lirc !*.f90 -o !*.x


      program ex11_1
      use DISLIN
      implicit none

      integer, parameter :: N = 200
      real, dimension (N,N) :: map
      real    :: FPI, dx, X, Y
      integer :: i, j

      FPI=3.1415926535/180.
      dx= 360./(N-1.)
      do i=1,N
        X=(i-1.)*dx
        do j=1,N
          Y=(j-1.)*dx
          map(i,j)=2*sin(X*FPI)*sin(Y*FPI)
        end do
      end do
      
      call SCRMOD('REVERS')
      call METAFL('CONS')
      call DISINI()
      call PAGERA()
      call HWFONT()

      call TITLIN('3-D Colour Plot of the Function',2)
      call TITLIN('F(X,Y) = 2 * SIN(X) * SIN(Y)',4)

      call name('X-axis','X')
      call name('Y-axis','Y')
      call name('Z-axis','Z')

      call INTAX()
      call AUTRES(N,N)
      call AXSPOS(300,1850)
      call AX3LEN(2200,1400,1400)

      call GRAF3(0.,360.,0.,90.,0.,360.,0.,90.,-2.,2.,-2.,1.)
      call CRVMAT(map,N,N,1,1)

      call HEIGHT(50)
      call TITLE()
      call MPAEPL(3)
      call DISFIN()
      STOP
      end program ex11_1

