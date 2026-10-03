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
!_________________________________________________________________________
! The result can be confirmed by choosing randomly 10-100 batches of 
! tetrahedrons on a unit sphere & checking the fraction with the desired
! property, by parallelized numerical procedures in Fortran95. 
!
! The generation of random angles was initially done by intrinsic fortran 
! procedure random_numbers(array), which was a slow singe-threaded black box.
! Now this is done on CPU/MIC by a OpenMP-multithreaded fortran code. 
! On th GPU it's done by calling Nvidia cuRAND library routines. 
!
! The rest (tetrahedron checking) is optimized ob CPU also by multithreading 
! directives w/compiler vectorization. 
! On GPU, the method is !$CUF directive-driven automatic loop kernel  
! generation. 
!
! The details on two computational platforms follow after 
! the text of the program that runs on GPUs. 
! 


 module vars
	implicit none
	real, parameter :: pi = atan(1.)*4., pi2 = 2.*pi
	integer,    parameter ::  N = 1024*1000*50  ! ~50 M
	integer(8), parameter :: NN = N,     iters = 100
	real, device, dimension(N) :: dth1, dth2, dth3, dph1, dph2, dph3
	real, device :: a1,a2,a3,b1,b2,b3,c1,c2,c3 
	real, device :: ct, st, D0, D1, D2, D3, D4
 end module vars


 program tetrahedrons
	use cudafor ! CUDA Fortran interface
	use curand	! CUDA random number lib interface
	use omp_lib
	use vars
	implicit none
	integer :: ok, i, iter, istat, dev, devs
	real :: p, p_av, t1 = 0., t2 = 0., t3 = 0.
	real (kind=8) :: t0, t00	
	integer(4) :: seed 
	type(curandGenerator) :: gen
! find and select all GPUs
	istat = cudaGetDeviceCount(devs)
  do dev = 0,devs-1
	istat = cudaSetDevice(dev)
! curand init
	seed = omp_get_wtime() ! call system_clock(seed); 
	print*,' seed',seed 
	istat = curandCreateGenerator(gen,CURAND_RNG_PSEUDO_DEFAULT) 
!	istat = curandCreateGenerator(gen,CURAND_RNG_PSEUDO_XORWOW)   ! 16.7x
!	istat = curandCreateGenerator(gen,CURAND_RNG_PSEUDO_MRG32K3A) ! 6.0x
!	istat = curandCreateGenerator(gen,CURAND_RNG_PSEUDO_MTGP32)   ! 9.8x
!	istat = curandCreateGenerator(gen,CURAND_RNG_PSEUDO_MT19937)  ! 14.5x
!	istat = curandCreateGenerator(gen,CURAND_RNG_PSEUDO_PHILOX4_32_10)!16.4x
!	istat = curandCreateGenerator(gen,CURAND_RNG_QUASI_SOBOL32)  ! wrong res
!	istat = curandCreateGenerator(gen,CURAND_RNG_QUASI_SCRAMBLED_SOBOL32)!,,
!	istat = curandCreateGenerator(gen,CURAND_RNG_QUASI_SOBOL64)! wrong
    istat = curandSetPseudoRandomGeneratorSeed (gen, seed)
	p_av = 0.
! 10 iterations of ~50 million tetrahedrons each 	
   do iter = 0,iters
!  vertices a,b,c are random on a sphere 
	t0 = omp_get_wtime() ! omp routine gets wall clock time w/resol. 1 us
! Generate NN floats or double on device
    istat = curandGenerateUniform (gen, dth1, NN) 
    istat = curandGenerateUniform (gen, dth2, NN) 
    istat = curandGenerateUniform (gen, dth3, NN) 
    istat = curandGenerateUniform (gen, dph1, NN) 
    istat = curandGenerateUniform (gen, dph2, NN) 
    istat = curandGenerateUniform (gen, dph3, NN) 
	istat = cudaDeviceSynchronize()
	if(iter>0) t1 = t1 + (omp_get_wtime() - t0)
	t0 = omp_get_wtime()
! counts tetrahedrons that incl. the center of the sphere
	ok = 0	 
!$cuf  kernel do <<<N/256,256>>>  
	do i = 1,N
 	 a3 = 1.-2.*dth1(i);   		st = sqrt(1.-a3*a3)  
	 a1 = cos(pi2*dph1(i))*st; 	a2 = sin(pi2*dph1(i))*st 
	 b3 = 1.-2.*dth2(i);   		st = sqrt(1.-b3*b3)   
	 b1 = cos(pi2*dph2(i))*st; 	b2 = sin(pi2*dph2(i))*st 
	 c3 = 1.-2.*dth3(i);   		st = sqrt(1.-c3*c3)   
	 c1 = cos(pi2*dph3(i))*st; 	c2 = sin(pi2*dph3(i))*st 
! compute five determinants
	 D1 = c1*b2 -b1*c2 
	 D2 = a1*c2 -a2*c1  
	 D3 =-a1*b2 +a2*b1
	 D4 = a1*(b2*c3-b3*c2) &
         -a2*(b1*c3-b3*c1) &
         +a3*(b1*c2-b2*c1)
	 D0 = D1 + D2 + D3 + D4
! counting those tetrahedrons which include the center of the sphere
	 if (D1*D0 >0 .and. D2*D0 >0 .and. D3*D0 >0 .and. D4*D0 >0) ok = ok +1	
	end do ! N
	 istat = cudaDeviceSynchronize()
	 if(iter>0) t2 = t2 + omp_get_wtime() - t0 
	 p = ok/real(N)
	 if(iter/20*20 == iter) print*,iter,' P',p
	 p_av = p_av + p/iters
   end do ! iterations	
! destroy curand handle
	istat = curandDestroyGenerator(gen)
! print results
	t3 = t1+t2
	print*,'gpu device #',dev
	print*,'one batch has N',1e-6*N,'M tetreah,',6e-9*N,'G rnd coord.'
	print*,'total #tetrah = ',iters,'*N=',real(iters)*N/1e9,'G'
	print*,'<P> = 1/8 +', p_av-0.125
	if (abs( p_av-0.125 ) > 1e-3) print*,'*** inaccuracy'
 	print*,iters*1e-6*N/t1,'M tetr./sec generation in t1=',t1,'s'
	print*,iters*1e-6*N/t2,'M tetr./sec checking   in t2=',t2,'s'
	print*,iters*1e-6*N/t3,'M tetr./sec gen&chk(GPU)in t=',t3,'s'
	print*,' which is faster than teraDc-3.f90(cpu)',0.45/(t3/iters),'x'
  end do ! devices
end program

! Appendices
!
! 1. Computational algebra of geometry:
!
!  Let the tetrahedron have vertices
!
!        V1 = (x1, y1, z1)
!        V2 = (x2, y2, z2)
!        V3 = (x3, y3, z3)
!        V4 = (x4, y4, z4)
!
! and the test point be
!
!        P = (x, y, z).
!
! Then the point P is in the tetrahedron if following five determinants 
! all have the same sign.
!
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


!__________________________________________________________________________
! 2. Numerical results on Nvidia GTX 1080ti (28 multiprocessors, 
! 	128 CUDA cores/MP)
!
! compiler of Fortran CUDA language is PGI Fortran v. 18.10
!
! pgf95 -mp -Mcuda=fastmath,cc35,cc50,cc60,fma,unroll,flushz,lineinfo 
! -ta=nvidia -tp=haswell -fast -Mcudalib=curand -O2 -Minfo=par 
! -mcmodel=medium  -I$DISLIN/pgf -ldislin  tetraDg.f95 -o tetraDg.x  \
! -L/usr/local/cuda-9.2/lib64 -lcufft -lcupti

! art-1[260]:~/avx$ tetraDg.x
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
! total #(tetrah.)=10N=    512000000 , <P> = 1/8 +   -3.047E-06
!    31.92639     M tetr./sec generation in t1    16.03689 s  (PGI!)
!    2210.692     M tetr./sec checking   in t2     0.23160 s (CUDA!!)
!    167.9527     M tetr./sec transfer   in t3     3.04848 s
!    26.45041     M tetr./sec transfer   in t     19.35698 s

! IMPROVED TO tetraDg-3:


!art-1[864]:~/avx$ tetraDg-3.x
!  seed            0
!           10  P   0.1249749    
!           20  P   0.1250260    
!           30  P   0.1250395        
!           80  P   0.1249649    
!           90  P   0.1250350    
!          100  P   0.1250165    
! gpu device #            0
! one batch has N    51.20000     M tetreah,   0.3072000     G rnd coord.
! total #(tetrah.)=                      100 *N=    5120.000     M
! <P> = 1/8 +   2.8014183E-06
!    11838.93     M tetr./sec generation in t1=   0.4324715     s
!    2315.857     M tetr./sec checking   in t2=    2.210845     s
!    1936.961     M tetr./sec gen&chk(GPU)in t=    2.643316     s
!  which faster than teraDc-3.f90(cpu)    17.02407     x
!  seed            0
!           10  P   0.1249749    
!           30  P   0.1250395    
!           40  P   0.1249323    
!           50  P   0.1249333    
!           90  P   0.1250350    
!          100  P   0.1250165    
! gpu device #            1
! one batch has N    51.20000     M tetreah,   0.3072000     G rnd coord.
! total #(tetrah.)=                      100 *N=    5120.000     M
! <P> = 1/8 +   2.8014183E-06
!    4170.627     M tetr./sec generation in t1=    1.227633     s
!    1110.029     M tetr./sec checking   in t2=    4.612493     s
!    876.6934     M tetr./sec gen&chk(GPU)in t=    5.840126     s
!  which faster than teraDc-3.f90(cpu)    7.705313     x



!__________________________________________________________________________
! 3. Numerical results on MIC (Knights Corner, 57 cores, 228 threads):
! 
! compilation details (intel ifort compiler v. 15.0.3.187)
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
! total #(tetrah.)=10N=   512010240 , <P> = 1/8 + 3.770E-06
!   15.26825      M tetr./sec generation in t1   33.53432 s
!   149.9071      M tetr./sec checking   in t2    3.41552 s

! IMPROVED TO 

!phi-1[266]:~/avx$ micnativeloadex tetraDc-3.micx -e "KMP_AFFINITY=compact"
!           1  P  0.1249444    
!           2  P  0.1251029    
!           3  P  0.1249901    
!           9  P  0.1249103    
!          10  P  0.1250242    
! total #(tetrah.)=          10 *N=   512.0103     M
! <P> = 1/8 + -8.0168247E-06
! total #(tetrah.)=10N=   512010240 , <P> = 1/8 + -8.0168247E-06
!   141.3532     M tetr./sec generation in t1   3.622205     s
!   158.5226     M tetr./sec checking   in t2   3.229887     s
!   74.72321     M tetr./sec gen & chk  in t2   6.852092     s
! slower than 0.32s tetraDg-3.f95(gpu)   21.41279     x


!___________________________________________________________________________
! 4. Results on CPU
!  = Intel i7-5820K (6 cores, 12 threads, 4 GHz overclock)
!
! $ ifort -qopenmp -O3 -no-prec-div -fp-model fast=2 -xHost -par-threshold20
! -align array64byte -mcmodel medium -shared-intel -fimf-domain-exclusion=8
! -qopt-report=5  -qopt-report-phase=vec  tetraDc.f90 -o tetraDc.x
!
! art-1[273]:~/avx$ tetraDc.x
!           1  P  0.1249607    
!           2  P  0.1250125    q
!           3  P  0.1250389    
!           4  P  0.1250301    
!           5  P  0.1250540    
!           6  P  0.1249538    
!           7  P  0.1249625    
!           8  P  0.1250430    
!           9  P  0.1249435    
!          10  P  0.1250387    
! total #(tetrah.)=10N=   512010240 , <P> = 1/8 +  3.7700E-06
!   11.76510      M tetr./sec generation in t1   43.51940 s
!   173.7800      M tetr./sec checking   in t2    2.94631 s

! IMPROVED TO

!art-1[866]:~/avx$ tetraDc-3.x
!           1  P  0.1249813    
!           2  P  0.1249722    
!           9  P  0.1250164    
!          10  P  0.1250077    
! total #(tetrah.)=10N=   512010240 , <P> = 1/8 + -5.3346157E-06
!   340.8908     M tetr./sec generation in t1   1.501977     s
!   176.7753     M tetr./sec checking   in t2   2.896390     s
!   116.4092     M tetr./sec gen & chk  in t2   4.398367     s
! slower than 0.32s tetraDg-3.f95(gpu)   13.74490     x


!-----------------------------------------------------------------------------
