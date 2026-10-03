!_______________________________________________________________________________
! Compilation on CentOS machines such as art-1, art-2 that use tcsh shell:
! $     pgf95d cudafor-laplace3-new
! where ~/.mycshrc has the following alias for pgf95d
! which passes to the pgf95 compiler lots of necessary and unecessary (for
! this program) compile options. 
!pgf95 -mp -Mcuda=fastmath,cc35,cc50,cc60,fma,unroll,flushz,lineinfo -ta=nvidia\
! -tp=haswell -fast -Mcudalib=curand -O2 -Minfo=par -mcmodel=medium \
! -I$DISLIN/pgf -ldislin !*.f95 -o !*.x -L/usr/local/cuda-9.2/lib64 \
! -lcufft -lcupti
!
! Compilation on Rocky 9 machines such as phi-10, which run bash shell: 
! $      nvf cudafor-laplace3-new
! where ~/.mybashrc defines the following function for nvf 
! function nvf { 
! nvfortran -Mpreprocess -mp -cuda gpu=ccnative,fma,zeroinit,unroll,fastmath,\
! lineinfo -acc -tp=sandybridge -O4 -mp=align -fast -Mcache_align \
! -mcmodel=medium -I$DISLIN/pgf -ldislin -cudalib=curand,cufft -lcufft \
! ./"$1".f95 -o ./"$1".nx }
!_______________________________________________________________________________

module mydata							! Large common-use arrays should be 
	use cudafor							! declared in a module (i.e. on heap) or 
    implicit none						! the OS stack increased sufficiently. 
	integer, parameter  :: pr = 8		! Precision 4=sp, 8=dp
	integer::  devi = 0
    integer, parameter :: N = 1024, M = 1024
	real(pr), parameter :: q = 0.2d0, q4 = 1d0-4d0*q
    integer :: nsteps, mo
    real(8) :: t0,t1
    real(pr) :: grid(0:N+1,0:M+1), grid2(0:N+1,0:M+1) 
    real(pr), device :: dgrid(0:N+1,0:M+1), dgrid2(0:N+1,0:M+1) 
	
   contains
	
   attributes(global) subroutine Laplace_gpu2(L,it)
	use cudafor				! use N/L threads in <<<.,N/8>>>
	integer, value :: it, L
	integer, device ::  i, j, k, p, ii
	i = Threadidx%x   ! i=1...N/L 
	j =  Blockidx%x   ! i=1...M
	if (mod(abs(it),2)==1) then
	  do k = 1,L
	  	ii = (i-1)*L + k
	    dgrid2(ii,j) = q4*dgrid(ii,j) + (dgrid(ii-1,j)+dgrid(ii+1,j) + & 
	  	 dgrid(ii,j-1)+dgrid(ii,j+1))*q
      end do
	else 
	  do k = 1,L
	  	ii = (i-1)*L + k	
	    dgrid(ii,j) = q4*dgrid2(ii,j) + &
        (dgrid2(ii-1,j)+dgrid2(ii+1,j)+(dgrid2(ii,j-1)+dgrid2(ii,j+1)))*q
      end do  
	end if 
!	if (i*j == 1) print*,' ij',i,j,' iter, p',it,p
end subroutine 


   attributes(global) subroutine Laplace_gpu0(it)
	use cudafor		
	integer, value :: it
	integer, device ::  i, j, p
	i = Threadidx%x   ! i=1...N 
	j =  Blockidx%x   ! i=1...M 
	if (mod(abs(it),2)==1) then  	
	  dgrid2(i,j) = q4*dgrid(i,j) + &
          (dgrid(i-1,j)+dgrid(i+1,j)+(dgrid(i,j-1)+dgrid(i,j+1)))*q
	else 
	  dgrid(i,j) = q4*dgrid2(i,j) + &
          (dgrid2(i-1,j)+dgrid2(i+1,j)+(dgrid2(i,j-1)+dgrid2(i,j+1)))*q
	end if 
!	if (i*j == 1) print*,' ij',i,j,' iter, p',it,p
end subroutine 


   attributes(global) subroutine Laplace_gpu1(it)
	use cudafor		
	integer, value :: it
	integer, device ::  i, j, p
	j = Threadidx%x   ! i=1...N 
	i =  Blockidx%x   ! i=1...M 
	if (mod(abs(it),2)==1) then  	
	  dgrid2(i,j) = q4*dgrid(i,j) + &
          (dgrid(i-1,j)+dgrid(i+1,j)+(dgrid(i,j-1)+dgrid(i,j+1)))*q
	else 
	  dgrid(i,j) = q4*dgrid2(i,j) + &
          (dgrid2(i-1,j)+dgrid2(i+1,j)+(dgrid2(i,j-1)+dgrid2(i,j+1)))*q
	end if 
!	if (i*j == 1) print*,' ij',i,j,' iter, p',it,p
end subroutine 

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


! CUF kernel version  - slow under nvfortran compiler
 subroutine Laplace_cuf(it)	
	use mydata	
	integer ::  i, j, it, ii, k
	if (mod(abs(it),2)==1 ) then
!$cuf kernel do(2) <<<N,M/2>>> 	
	 do j = 1,M
	  do i = 1,N
	   do k = 1,2
	    ii = (i-1)*2 + k
	    dgrid2(ii,j) = q4*dgrid(ii,j) + (dgrid(ii-1,j)+dgrid(ii+1,j) + & 
	  	 dgrid(ii,j-1)+dgrid(ii,j+1))*q
      	   end do
           end do 
	  end do      	   
	else 
!$cuf  kernel do(2) <<<N,M/2>>> 	
	 do j = 1,M
	  do i = 1,N 
	   do k = 1,2
	    ii = (i-1)*2 + k	
	    dgrid(ii,j) = q4*dgrid2(ii,j) + &
            (dgrid2(ii-1,j)+dgrid2(ii+1,j)+(dgrid2(ii,j-1)+dgrid2(ii,j+1)))*q
            end do     
           end do 
	  end do     
	end if 
!	if (i*j == 1) print*,' ij',i,j,' iter, p',it,p
 end subroutine Laplace_cuf


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


!============================================================================
!________________________________________________________________________
! main (driver) program
!
! Laplace stencil smoothing of a 1k x 1k image (float array)
!________________________________________________________________________

program smooth
    use omp_lib 
    use mydata
    character(len=1), parameter :: ESC = achar(27)
    character(len=*), parameter :: RESET   = ESC // '[0m'
    character(len=*), parameter :: RED     = ESC // '[31m', GREEN   = ESC // '[32m'
    character(len=*), parameter :: YELLOW  = ESC // '[33m', BLUE    = ESC // '[34m'
	!real :: g 
	integer :: istat
	nsteps = 100   

do devi = 0,1        !  GPU devices
        if (pr==8) print*, GREEN//'double'//RESET//' precision, device',devi
	if (pr==4) print*, GREEN//'single'//RESET//' precision, device',devi

!----------------- CUDA kernel Laplace_gpu2  N/L threads: 1st index
	if(cudaSetDevice(devi) /=0) then 
		print*,'dev not set!'; stop
	end if
! initialize grid to 0 and subgrid to 1 
	grid = 0.d0;  	grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0
! transfer to device
	dgrid = grid
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace_gpu2 <<< M,(N/4) >>> (4,iter)   ! i.e.,  L=4
	if(cudaDeviceSynchronize() /= 0) print*,iter,' nonsync 2' 
  end do ! iter
! time and print
	t1 = (omp_get_wtime()-t0)/nsteps
! transfer to host	
	grid = dgrid	
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' CUDA kernel 2'


!----------------- CUDA kernel Laplace_gpu0  threads: 1st index
	if(cudaSetDevice(devi) /=0) print*,'dev not set!'
! initialize grid to 0 and subgrid to 1 
	grid = 0.d0;  	grid(100,100) = 3.
    grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0
! transfer to device
	dgrid = grid
!	dgrid(100,100) = 7.; grid2 = dgrid; !print*,' 100,100:',grid2(100,100)
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace_gpu0 <<< M,N >>>(iter)
	if(cudaDeviceSynchronize() /= 0) print*,iter,' nonsync 0' 
  end do ! iter
! time and print
	t1 = (omp_get_wtime()-t0)/nsteps
! transfer to host	
	grid = dgrid	
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' CUDA kernel 0'


!------------------- CUDA kernel Laplace_gpu1  threads: 2nd index
	if(cudaSetDevice(devi) /=0) print*,'dev not set!'
! initialize grid
	grid = 0.d0
	grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0
! transfer to device
	dgrid = grid
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace_gpu1 <<< M,N >>>(iter)
	if(cudaDeviceSynchronize() /= 0) print*,iter,' nonsync 1' 
  end do ! iter
! time and print
	t1 = (omp_get_wtime()-t0)/nsteps
! transfer to host	
	grid = dgrid	
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' CUDA kernel 1'

!------------------ CUDA kernel Laplace_cuf  <<M,N>> $cuf
	if(cudaSetDevice(devi) /=0) print*,'dev not set!'
! initialize grid
	grid = 0.d0
	grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0
! transfer to device
	dgrid = grid
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace_cuf (iter)
	if(cudaDeviceSynchronize() /= 0) print*,iter,' nonsync 1' 
  end do ! iter
! time and print
	t1 = (omp_get_wtime()-t0)/nsteps
! transfer to host	
	grid = dgrid	
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' CUDA $cuf '
    
    
!------------------- Host code w/OMP + slices  
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
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' Host OMP slices'


!-------------------- Host code w/OMP  
! initialize grid
	grid = 0.d0
	grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0
	grid(1,1) = 3.d0
! compute on host
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace0(iter)
  end do ! iter
	t1 = (omp_get_wtime()-t0)/nsteps
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' host OMP'

!------------------ Plain host (i.e. CPU) code  
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
	
! cite Python results w/o running the scripts
	t1 = 0.00372 ! timing of 1 M pixel equivalent. 466x680 image via NumPy
    print*,'t=',real(t1),int(1./t1),'fps,  Numpy dp'
	print*,'t=',real(t1*42),'         6.4 fps,  plain Python'
	
end do 
		
end program smooth
 
 
