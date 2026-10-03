! Problem: What is the probability that randomly chosen 4 points
! on a sphere form a tetrahedron, which encloses the center of the sphere?
! Ans.: 1/8
!
! Analytical proof (c) P. Artymowicz
!
! See http://mathworld.wolfram.com/SphericalTriangle.html
! for the area of a spherical triangle with angles (not sides)
! equal A,B,C. On a unit sphere, the triangle has angles between 
! zero and pi, and occupies the following fraction of the full sphere
! p = (A+B+C-pi)/(4 pi) = (A+B+C)/(4 pi) -1/4.
! (Notice that the maximum p is 1/2, not 1, since we do not consider 
! tetrahedrons wrapped around into the other hemisphere (on a sphere
! 3 points define two complementary spherical triangles).
!
! In order to enclose the center, the forth vertex must be located in a 
! solid angle 'cone' which is the point-symmetric reflection w.r.t the center
! of the sphere of the cone spanned by three vertices (one triangular wall 
! of tetrahedron). Make a sketch to convince yourself. The same idea works in
! any number of dimensions, e.g. 2, with triangles inscribed in circles.
!  
! By the symmetry of the problem, all angles are statistically equivalent. 
! If the top point d of the tetrahedron on top pf the sphere at (0,0,1), 
! then the top angle A is simply the azimuthal angle or longitude on the 
! sphere. Each angle, e.g. A, is uniformly distributed with probability density 
! dA/pi from 0 to pi, generating after triple integration over a product 
! of increments dA/pi, dB/pi, and dC/pi, an average fractional area of 
! the spherical triangle (one wall of tetrah.) relative to the sphere: 
! P =  -1/4 + integral_0^pi  3A/(4pi) dA/pi. 
! Finally, the chance of a random 4th point to land in the desired
! triangular solid angle cone is 
! P =  -1/4 + 3/8 = 1/8,     Q.E.D.
!
! The result can be confirmed by choosing randomly ~half a billion
! tetrahedrons on a unit sphere and checking the fraction with the desired
! property, by parallelized numerical procedure in Fortran95. 
!
! The generation of random angles is done by intrinsic Intel fortran compiler
! procedure random_numbers(array), which is a black box, and possibly not
! the fastest possible. On the other habd, checking of inclusion of point
! (0,0,0) in a tetrahedron is optimized by multithreading with OpenMP 
! directives, while the compiler additionally vectorizes parts of the code.
!
! The method and tests on two computational platforms follow after 
! the text of the program. 
! Let's begin with the CPU/MIC (many integrated cores) version. 
! Importantly, the 57-core and 6-core processors use the same source code
! given in its entirety above; only one compilation flag is different. 
! They get exactly the same results down to the last digit. 
! 

 module vars3
	use omp_lib
	real, parameter    :: pi = atan(1.)*4., pi2 = 2.*pi
	integer, parameter :: N = (1024*1000*50/(12*224)+1)*(12*224) ! 50 M 
	real, dimension(N) :: th1, th2, th3, ph1, ph2, ph3
	real, dimension(3) :: a,b,c 
	real 			   :: ct, st, D0, D1, D2, D3, D4
    !$omp threadprivate(a,b,c,ct,st,D0,D1,D2,D3,D4) 
 contains 

  subroutine rand6arr(a1,a2,a3,f4,f5,f6)
!
! fills 6 arrays of size N with uniform random numbers 
! Based on	CPU/MIC function ran (idum)
! Replacement for ran1.f from F77 Num Recipes.
! “Minimal” random number generator of Park and Miller combined with a 
! Marsaglia shift sequence. Returns a uniform random deviate from 0.0 to 1.0 
! (exclusive of the endpoints). This fully portable, scalar generator has the
! “traditional” (not Fortran 90) calling sequence with a random deviate as
! the returned function value: call with idum a negative integer to 
! initialize; thereafter, do not alter idum except to reinitialize. 
! The period of this generator is about 3.1e18.
!
	implicit none
	real, dimension(N) :: a1,a2,a3,f4,f5,f6 
!	size of arr = N must be a known integer par., a multiple of thread #
	integer, parameter :: IA=16807,IM=2147483647,IQ=127773,IR=2836
	real, parameter :: am = nearest(1.0,-1.0)/IM
	integer :: ix=-1, iy=-1
	integer :: k, i, iarr, idum, ithr, nthr
	integer(4) :: cpu0, cpu1
	real(kind=8) :: t0
	t0 =  omp_get_wtime();  call system_clock(cpu0)
	cpu1 = cpu0 - (cpu0/64000*64000)	!; 	print*,'cpu1',cpu1
!--- parallel region fills 1/nthr of the 6 arrays 
!$omp parallel firstprivate (ix,iy,k,i,iarr,idum,ithr,nthr,cpu1)
 	ithr = omp_get_thread_num()
	nthr = omp_get_num_threads(); if(nthr < 12) stop 'nthr<12'
	idum = abs(int((omp_get_wtime()-t0)*1d7) + cpu1 & 
	  	+12 +ithr*(ithr+14)) ! thread-unique, positive seed
!	idum = 123 ! positive seed <<<
!	print*,ithr,' of',nthr,' seed',idum,' cpu1',cpu1
! RND # generator mandatory init	
	iy = ior(ieor(888889999,(idum)),1)
	ix = ieor(777755555,(idum))
	idum = (idum)+1
! each thread does its own chunk of 6 arrays
    do i = 1+ithr*(N/nthr),(1+ithr)*(N/nthr) !  1<i<N for all i
	do iarr = 1,6
! RND # generator 
	ix = ieor(ix,ishft(ix,13))
	ix = ieor(ix,ishft(ix,-17))
	ix = ieor(ix,ishft(ix,5))
	k  = iy/IQ
	iy = IA*(iy-k*IQ)-IR*k
	if (iy < 0) iy = iy + IM
! final scaling
	if (iarr==1) a1(i) = am*ior(iand(IM,ieor(ix,iy)),1) 
	if (iarr==2) a2(i) = am*ior(iand(IM,ieor(ix,iy)),1) 
	if (iarr==3) a3(i) = am*ior(iand(IM,ieor(ix,iy)),1) 
	if (iarr==4) f4(i) = am*ior(iand(IM,ieor(ix,iy)),1) 
	if (iarr==5) f5(i) = am*ior(iand(IM,ieor(ix,iy)),1) 
	if (iarr==6) f6(i) = am*ior(iand(IM,ieor(ix,iy)),1) 
	end do ! i; end chunk belonging to thread	
	end do ! 6 arrays
!$omp end parallel 
	end subroutine 
 end module vars3


 program tetrahedrons
!
	use vars3
	integer :: ok, i, iter 
	real :: p, p_av = 0., t1 = 0., t2 = 0., t3
	real(kind=8) :: t0 
! 10 iterations of ~54 million tetrahedrons each 
   do iter = 0,10
!  vertices a,b,c are random on a sphere 
	t0 = omp_get_wtime() ! omp routine gets wall clock time w/resol. 1 us
	call rand6arr(th1,th2,th3,ph1,ph2,ph3) 
	if(iter>0) t1 = t1 + (omp_get_wtime() - t0)
! counts tetrahedrons that incl. the center of the sphere	
	ok = 0 
	t0 = omp_get_wtime()
!$omp parallel do reduction(+:ok)
	do i = 1,N
	 ct = 1.-2.*th1(i);   st = sqrt(1.-ct*ct) ! cos and sin of colatitude
	 a = (/ cos(pi2*ph1(i))*st, sin(pi2*ph1(i))*st, ct /)
	 ct = 1.-2.*th2(i);   st = sqrt(1.-ct*ct)   
	 b = (/ cos(pi2*ph2(i))*st, sin(pi2*ph2(i))*st, ct /)
	 ct = 1.-2.*th3(i);   st = sqrt(1.-ct*ct)   
	 c = (/ cos(pi2*ph3(i))*st, sin(pi2*ph3(i))*st, ct /)
! compute five determinants
	 D1 = c(1)*b(2) -b(1)*c(2) 
	 D2 = a(1)*c(2) -a(2)*c(1)  
	 D3 =-a(1)*b(2) +a(2)*b(1)
	 D4 = a(1)*(b(2)*c(3)-b(3)*c(2)) &
         -a(2)*(b(1)*c(3)-b(3)*c(1)) &
         +a(3)*(b(1)*c(2)-b(2)*c(1))
	 D0 = D1 + D2 + D3 + D4
! counting those tetrahedrons which include the center of the sphere
	 if (D1*D0 >0 .and. D2*D0 >0 .and. D3*D0 >0 .and. D4*D0 >0) ok = ok+1	
	end do ! N
!$omp end parallel do 
	if(iter>0) t2 = t2 + (omp_get_wtime() - t0) 
	p = ok/real(N)
	print*,iter,' P',p
	p_av = p_av + p/10
  end do
	t3 = t1 + t2
	print*,'total #(tetrah.)=',10,'*N=',10*N/1e6,'M'
	print*,'<P> = 1/8 +', p_av-0.125
	print*,'total #(tetrah.)=10N=',10*N,', <P> = 1/8 +', p_av-0.125
	print*,10e-6*N/t1,'M tetr./sec generation in t1',t1,'s'
	print*,10e-6*N/t2,'M tetr./sec checking   in t2',t2,'s'	
	print*,10e-6*N/t3,'M tetr./sec gen & chk  in t2',t3,'s'	
	print*,'slower than 0.32s tetraDg-3.f95(gpu)',t3/0.32,'x'
end program

! comments: 
!  Let the tetrahedron have vertices
!        V1 = (x1, y1, z1)
!        V2 = (x2, y2, z2)
!        V3 = (x3, y3, z3)
!        V4 = (x4, y4, z4)
! and the test point be     P = (x, y, z).
! Then the point P is in the tetrahedron if following five determinants 
! all have the same sign.
!             |x1 y1 z1 1|
!        D0 = |x2 y2 z2 1|
!             |x3 y3 z3 1|
!             |x4 y4 z4 1|
!
!             |x  y  z  1|
!        D1 = |x2 y2 z2 1|
!             |x3 y3 z3 1|
!             |x4 y4 z4 1|
!
!             |x1 y1 z1 1|
!        D2 = |x  y  z  1|
!             |x3 y3 z3 1|
!             |x4 y4 z4 1|
!
!             |x1 y1 z1 1|
!        D3 = |x2 y2 z2 1|
!             |x  y  z  1|
!             |x4 y4 z4 1|
!
!             |x1 y1 z1 1|
!        D4 = |x2 y2 z2 1|
!             |x3 y3 z3 1|
!             |x  y  z  1|
!
! In the inscribed random tetrahedron problem, x=y=z=0 (center of the sphere)
! and x4=y4=0, z4=1 (top of the tetrahedron is fixed at d=(0,0,1).
! We also have a = (x1,y1,z1), b = (x2,y2,z2) and c = (x3,y3,z3).
! 
! Numerical results on MIC (Knights Corner):
! 
! compilation details
! $ ifort -qopenmp -O3 -no-prec-div -fp-model fast=2 -mmic -par-threshold20
! -align array64byte -mcmodel medium -shared-intel -fimf-domain-exclusion=8
! -qopt-report=5  -qopt-report-phase=vec  tetraDc.f90 -o tetraDc.micx
!
! On Xeon Phi (224 threads)
! 
! phi-1[190]:~/avx$ micnativeloadex tetraDc.micx -e "KMP_AFFINITY=compact"
!           1  P  0.1249607    
!           2  P  0.1250125    
!           3  P  0.1250389    
!           4  P  0.1250301    
!           5  P  0.1250540    
!           6  P  0.1249539    
!           7  P  0.1249625    
!           8  P  0.1250430    
!           9  P  0.1249435    
!          10  P  0.1250387    
! total #(tetrah.)=10N=   512010240 , <P> = 1/8 +  3.7699938E-06
!   15.26825      M tetr./sec generation in t1   33.53432     s
!   149.9071      M tetr./sec checking   in t2   3.415517     s


! $ ifort -qopenmp -O3 -no-prec-div -fp-model fast=2 -xHost -par-threshold20
! -align array64byte -mcmodel medium -shared-intel -fimf-domain-exclusion=8
! -qopt-report=5  -qopt-report-phase=vec  tetraDc.f90 -o tetraDc.x
!
! On an i7-5820K Xeon cpu (12 threads, 4 GHz clock) 
! art-1[273]:~/avx$ tetraDc.x
!           1  P  0.1249607    
!           2  P  0.1250125    
!           3  P  0.1250389    
!           4  P  0.1250301    
!           5  P  0.1250540    
!           6  P  0.1249538    
!           7  P  0.1249625    
!           8  P  0.1250430    
!           9  P  0.1249435    
!          10  P  0.1250387    
! total #(tetrah.)=10N=   512010240 , <P> = 1/8 +  3.7699938E-06
!   11.76510      M tetr./sec generation in t1   43.51940     s
!   173.7800      M tetr./sec checking   in t2   2.946314     s

!
! CPU version of fortran-standard point generation runs 33% slower than MIC
! version: in 43.5 s vs. 33.5 s.
! MIC version of OMP'd checking of tetrahedrons runs 16% slower than CPU
! version: in 3.42 s vs. 2.95 s. Throughput on CPU is 174 M tetr./s.

! -----compare with the GPU version (CUDA Fortran, PGI compiler)
! on Nvidia gtx 1080ti graphics card 
! art-1[291]:~/avx$ tetraDg.x
!            1  P   0.1250303    
!            2  P   0.1249688    
!            3  P   0.1250295    
!            4  P   0.1250226    
!            5  P   0.1249475    
!            6  P   0.1249093    
!            7  P   0.1249561    
!            8  P   0.1250123    
!            9  P   0.1250809    
!           10  P   0.1250123    
! total #(tetrah.)=10N=    512000000 , <P> = 1/8 +  -3.0472875E-06
!    31.92639      M tetr./sec generation in t1    16.03689     s
!    2210.692      M tetr./sec checking   in t2   0.2316017     s (!!!)
!    167.9527      M tetr./sec transfer   in t3    3.048477     s

!  
