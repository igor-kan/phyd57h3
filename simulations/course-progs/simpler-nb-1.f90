!  loop example
!
! do %limit stacksize 999m before running program to increase linux stack size, 
! or you may get a segfault.
! Compilation:
! art-1[232]:~/avx$ ifort -O{2,1,2,3} -openmp simpler-nb-0.f90 -o simpler-nb-0.x

	use omp_lib
	implicit none
	integer, parameter :: N = 30000000, prec = 4 
	integer :: i, iter
	real(kind=prec) :: tab(N,6), gflops
	real(kind=8) :: t0, t1

! initialize 
	tab = 0.
	tab(100:120,1:6) = 1.  
    t0 = omp_get_wtime()
! run 10 times 
   do iter = 1,10
	do i = 1,N
		tab(i,4) = tab(i,1)**2 - tab(i,2) + tab(1+i/2, 5)
	end do 
   end do 
	t1 = omp_get_wtime() - t0
	gflops = 4*10*1e-9*N/t1
    print*,' done in ', 1000*t1,'ms'
    print*,' throughput', gflops,' GFLOPs << theor. limit'
	print*,' if bandwidth limited:', gflops*prec, ' GB/s '
end



