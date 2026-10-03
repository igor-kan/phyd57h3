! Brute force search for solutions to "711" puzzle for 
! S=711 and a whole wide range of other numbers. 
! x+y+z+r = S         hence:  r = S-x-y-z
! x*y*z*(S-x-y-z) = S *  1 million! All prices are in cents
! All combinations such that x <= y <= z  are generated
! but only if  x <= y <= z <= r the equation is checked.
! permutations are not computed, saving time 
!
! compile as:   % gfortran -O2 711s-brute.f95 -o 711s-brute.gf.x
! run as:       % 711s-brute.gf.x  in tcsh or if dir . is in $PATH 
!     or        % ./711s-brute.gf.x   in a standard bash shell 
! if you want to use the ifort compiler, change the extension to .f90
! somehow Intel compiler doesn't like the file format when it's .f95 :-(, 
! then compile as   % ifort -O2 711-brute.f90 -o 711s-brute.ifo.x and run.
  implicit none
  integer ::  x,y,z,r, S
  integer (kind=8) n	! counter, 4B int will overflow, needs 8B (long int)
  n = 0
  do S = 300, 2030  ! check sum of prices from 300 to 2030 cents
   do x = 1, S-3		 
	do y = x, S-2-x   
	 do z = y, S-1-x-y
	  r = S-x-y-z
	  if (r < z) cycle	 ! cycle means skip the rest of the innermost loop
	  n = n + 1
	  if (x*y*z*r == S*1000000) print*,'x,y,z,r',x,y,z,r,' cents, S=',S
	 end do
    end do
   end do
  end do 
  print*, 'checked in detail', n, '  cases '
end 
