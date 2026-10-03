!________________________________________________________________________________
! compilation:
! pgf95d cudafor-laplace-sp/dp 
! where 
!pgf95 -mp -Mcuda=fastmath,cc35,cc50,cc60,fma,unroll,flushz,lineinfo -ta=nvidia \
! -tp=haswell -fast -Mcudalib=curand -O2 -Minfo=par -mcmodel=medium \
! -I$DISLIN/pgf -ldislin !*.f95 -o !*.x -L/usr/local/cuda-9.2/lib64 \
! -lcufft -lcupti
!_________________________________________________________________________________

module mydata
	use cudafor
    implicit none
	integer, parameter :: pr = 4
    integer, parameter :: N = 1024, M = 1024
	real(pr), parameter :: q = 0.2d0, q4 = 1d0-4d0*q
    integer :: nsteps, mo
    real(8) :: t0,t1
    real(pr) :: grid(0:N+1,0:M+1), grid2(0:N+1,0:M+1) 
    real(pr), device :: dgrid(0:N+1,0:M+1), dgrid2(0:N+1,0:M+1) 

   contains
	
   attributes(global) subroutine Laplace(it)
	use cudafor		
	integer, value :: it
	integer, device ::  i, j, p
	i = Threadidx%x   ! j=1...N 
	j =  Blockidx%x   ! i=1...M 
	if (mod(abs(it),2)==1) then  	
	   dgrid2(i,j) = q4*dgrid(i,j) + &
       (dgrid(i-1,j)+dgrid(i+1,j)+(dgrid(i,j-1)+dgrid(i,j+1)))*q
	else 
	   dgrid(i,j) = q4*dgrid2(i,j) + &
       (dgrid2(i-1,j)+dgrid2(i+1,j)+(dgrid2(i,j-1)+dgrid2(i,j+1)))*q
	end if 
!	if (i*j == 1) print*,' ij',i,j,' iter, p',it,p
end subroutine Laplace

end module mydata


! slices w/omp
 subroutine Laplace0s(it)
	use mydata	
	integer ::  i, j, it ! step # it should be odd the first time 
	if (mod(abs(it),2)==1) then
!$omp parallel do 
	 do i = 1,N
	   grid2(i,1:M) = q4*grid(i,1:M) + &
       (grid(i,0:M-1)+grid(i,2:M+1)+grid(i-1,1:M)+grid(i+1,1:M))*q
	 end do
	else 
!$omp parallel do    
	  do i = 1,N
	   grid(i,1:M) = q4*grid2(i,1:M) + &
       (grid2(i,0:M-1)+grid2(i,2:M+1)+grid2(i-1,1:M)+grid2(i+1,1:M))*q
	  end do
	end if 
 end subroutine Laplace0s


! CUF kernel version  - not in use with PGI compiler
 subroutine Laplace2(it)	
	use mydata	
	integer ::  i, j, it
	if (mod(abs(it),2)==1 ) then
!$cuf kernel do(2) <<<N,M>>> 	
	 do j = 1,M
	  do i = 1,N
	   dgrid2(i,j) = q4*dgrid(i,j) + &
       (dgrid(i-1,j)+dgrid(i+1,j)+(dgrid(i,j-1)+dgrid(i,j+1)))*q
	  end do
	 end do
	else 
!$cuf  kernel do(2) <<<N,M>>> 	
	 do j = 1,M
	  do i = 1,N
	   dgrid(i,j) = q4*dgrid2(i,j) + &
       (dgrid2(i-1,j)+dgrid2(i+1,j)+(dgrid2(i,j-1)+dgrid2(i,j+1)))*q
	  end do
	 end do
	end if 
!	if (i*j == 1) print*,' ij',i,j,' iter, p',it,p
 end subroutine Laplace2


! OMP version 
 subroutine Laplace0(it)
	use mydata	
	integer ::  i, j, it 
	if (mod(abs(it),2)==1) then 
!$omp parallel do collapse(1)
	 do j = 1,M
	  do i = 1,N
	   grid2(i,j) = q4*grid(i,j) + &
       (grid(i-1,j)+grid(i+1,j)+(grid(i,j-1)+grid(i,j+1)))*q
	  end do
	 end do
	else 
!$omp parallel do collapse(2)
	 do j = 1,M
	  do i = 1,N
	   grid(i,j) = q4*grid2(i,j) + &
       (grid2(i-1,j)+grid2(i+1,j)+(grid2(i,j-1)+grid2(i,j+1)))*q
	  end do
	 end do
	end if 
!	if (i*j == 1) print*,' ij',i,j,' iter, p',it,p
 end subroutine Laplace0


! straight PGI fortran-compiled version 
 subroutine Laplace00(it)
	use mydata	
	integer ::  i, j, it
	if (mod(abs(it),2)==1) then
	 do j = 1,M
	  do i = 1,N
	   grid2(i,j) = q4*grid(i,j) + &
       (grid(i-1,j)+grid(i+1,j)+(grid(i,j-1)+grid(i,j+1)))*q
	  end do
	 end do
	else 
	 do j = 1,M
	  do i = 1,N
	   grid(i,j) = q4*grid2(i,j) + &
       (grid2(i-1,j)+grid2(i+1,j)+(grid2(i,j-1)+grid2(i,j+1)))*q
	  end do
	 end do
	end if 
 end subroutine Laplace00


!__________________
! main program
!__________________

program smooth
    use omp_lib 
    use mydata
	!real :: g 
	integer :: istat    
! params
    nsteps = 100    

! CUDA kernel dev 0
	if(cudaSetDevice(1) /=0) print*,'dev not set!'
! initialize grid
	grid = 0.d0
    grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0
! transfer to device
	dgrid = grid
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace <<<N,M>>>(iter)
	if(cudaDeviceSynchronize() /= 0) print*,iter,' nonsync' 
  end do ! iter
! time and print
	t1 = (omp_get_wtime()-t0)/nsteps
! transfer to host	
	grid = dgrid	
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' CUDA kernel 0'


! CUDA kernel dev 1
	if(cudaSetDevice(1) /=0) print*,'dev not set!'
! initialize grid
	grid = 0.d0
    grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0
! transfer to device
	dgrid = grid
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace <<<N,M>>>(iter)
	if(cudaDeviceSynchronize() /= 0) print*,iter,' nonsync' 
  end do ! iter
! time and print
	t1 = (omp_get_wtime()-t0)/nsteps
! transfer to host	
	grid = dgrid	
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' CUDA kernel 1'

! host code w/OMP + slices  
! initialize grid
	grid = 0.d0
    grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0
! compute on host
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace0s(iter)
  end do ! iter
	t1 = (omp_get_wtime()-t0)/nsteps
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' host OMP slices'


! host code w/OMP  
! initialize grid
	grid = 0.d0
    grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0
! compute on host
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace0(iter)
  end do ! iter
	t1 = (omp_get_wtime()-t0)/nsteps
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' host OMP'

! straight host code  
! initialize grid
	grid = 0.d0
    grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0  
  call omp_set_num_threads(1)  
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace00(iter)
  end do ! iter
	t1 = (omp_get_wtime()-t0)/nsteps
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' host'
	
! cite Python results
	t1 = 0.00372 ! 1 M pixels equiv. timing. 466x680 image via NumPy
    print*,'t=',real(t1),int(1./t1),'fps,  Numpy dp'
	print*,'t=',real(t1*42),'         6.4 fps,  Python'

end program smooth
 
 
