!________________________________________________________________________________
! compilation:
! forcpu cudafor-laplace-sp 
! where 
! ifort -qopenmp -O3 -no-prec-div -fp-model fast=2 -xHost -par-threshold20 
! -align array64byte -mcmodel medium -shared-intel -fimf-domain-exclusion=8 
! -qopt-report=5  -qopt-report-phase=vec -ldislin -I$DISLIN/ifc 
! -L/opt/intel/composer_xe_2015.3.187/compiler/lib/intel64 -lirc !*.f90 -o !*.x
!_________________________________________________________________________________

module mydata
	use omp_lib
    implicit none
    integer, parameter :: N = 1024, M = 1024
	real(8), parameter :: q = 0.2d0, q4 = 1d0-4d0*q
    real(8) :: t0,t1
    real(8) :: grid(0:N+1,0:M+1), grid2(0:N+1,0:M+1) 

 contains
	
 subroutine init()
	grid = 0d0;  grid(N/2-10:N/2+10,M/2-12:M/2+12) = 1.d0	
 end subroutine init

end module mydata


! OMP version 

 subroutine Laplace0(it)
	use mydata	
	integer ::  i, j, it ! step # it should be odd the first time 
	if (mod(abs(it),2) == 1) then
!$omp parallel do collapse(2)
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
 

 subroutine Laplace0i(it)
	use mydata	
	integer ::  i, j, it ! step # it should be odd the first time 
	if (mod(abs(it),2) == 1) then
!$omp parallel do collapse(2)
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
 end subroutine Laplace0i
 

! straight pgf or ifor fortran-compiled version 
 subroutine Laplace00(it)
	use mydata	
	integer ::  i, j, it ! step # it should be odd the first time 
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


! square slices
 subroutine Laplace0sq(it)
	use mydata	
	integer ::  i, j, it ! step # it should be odd the first time 
	if (mod(abs(it),2)==1) then 
	   grid2(1:N,1:M) = q4*grid(1:N,1:M) + &
       (grid(1:N,0:M-1)+grid(1:N,2:M+1)+grid(0:N-1,1:M)+grid(2:N+1,1:M))*q
	else 
	   grid(1:N,1:M) = q4*grid2(1:N,1:M) + &
       (grid2(1:N,0:M-1)+grid2(1:N,2:M+1)+grid2(0:N-1,1:M)+grid2(2:N+1,1:M))*q
	end if 
 end subroutine Laplace0sq

!__________________
! main program
!__________________

program smooth   
    use mydata
	implicit none
	real :: g
	integer :: iter, istat, nsteps   
! params
    nsteps = 100    
 
! host code w/OMP  
  call init()
! compute on host
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace0(iter)
  end do ! iter
	t1 = (omp_get_wtime()-t0)/nsteps
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' host OMP'

! host code w/OMP  
  call init()
! compute on host
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace0i(iter)
  end do ! iter
	t1 = (omp_get_wtime()-t0)/nsteps
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' host OMP i'
	
! straight host code  
   call init()
!  call omp_set_num_threads(1)  
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace00(iter)
  end do ! iter
	t1 = (omp_get_wtime()-t0)/nsteps
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' host'

!  host code  with slices, omp
   call init()
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace0s(iter)
  end do ! iter
	t1 = (omp_get_wtime()-t0)/nsteps
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' host slices'

!  host code with square slices
   call init()
  do iter = -3,nsteps
	if(iter==1) t0 = omp_get_wtime()
	call Laplace0sq(iter)
  end do ! iter
	t1 = (omp_get_wtime()-t0)/nsteps
	g = grid(N/2-10,M/2-10)
    print*,'t=',real(t1),int(1./t1),'fps,  val=',g,' host squares'

! cite Python results
	t1 = 0.00372 ! 1 M pixels equiv. timing. 466x680 image via NumPy
    print*,'t=',real(t1),int(1./t1),'fps,  Numpy'
    print*,'t=',real(t1*42),int(1./t1/42),'fps,  Python'


end program smooth

! results: no influence of single vs double precision
! this may mean that the bottleneck is starting kernels/threads
 

 
