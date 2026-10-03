! Intelligent brute force search for solutions to 711 puzzle
! x+y+z+r = 711,
! x*y*z*(711-x-y-z) = 711*10**6 = 79 2^6 3^2 5^6 
! All prices are in cents.
! Let x be the only price divisible by 79; x = k*79, k=1..9
! actually only k = 1,2,3,4,5,6  allowed 
! because k=8 cannot satisfy 8*y*z*(79-y-z)=9e6; since 79**3 < 9e6/8,
! and k=7 is excluded by prime decomposition of the product. 
! y,z numbers must be in the form 
! y,z = 2^a 3^b 5^c => less than 630 possibilities ea.
! a=0..6, b=0..2, c=0..4, so 7*3*5 = 3*35 = 105 possibilities ea. only
! max 6*105^2 ~66k cases to generate so OK, less if permutations skipped
	
  integer :: i,j,k,l,m,n,  x,y,z,r, yz(105)

! precompute all possible y or z values
	m = 0
	do i = 0,6
	 do j = 0,2
	  do k = 0,4
	   m = m + 1
	   yz(m) = 2**i * 3**j * 5**k
	  end do 
 	 end do 
	end do 

! for all possible x
   n = 0
   do k = 1,6
    x = k*79
	l = 711-x
! check all y < z < r pairs 
	do i = 1,105
	 y = yz(i)
	 m = l-y
	 do j = 1,105 
	  z = yz(j)
	  r = m-z
	  if (y > z .or. z > r) cycle
	  n = n+1
	  if (k*y*z*r==9000000) print*,'x,y,z,r',x,y,z,r,' cents'
	 end do
    end do
   end do
   print*, ' checked',n,'  cases' 
end
