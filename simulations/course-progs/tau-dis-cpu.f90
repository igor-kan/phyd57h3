! program tau-dis.f90 
! IRI = Irradiation Instability in a Keplerian, optically thick disk 
! (c) P. Artymowicz 2019-2025 (this is a modified version)
!
!  includes dislin graphics, 
!  compiles with ifort  (all options not necessary..)
!  ifort -qopenmp -O3 -no-prec-div -fp-model fast=2 -xHost \ 
!   -L$DISLIN10 -ldislin10 -I$DISLIN10/ifc \
!   -L/opt/intel/composer_xe_2015.3.187/compiler/lib/intel64 -lirc !*.f90 -o !*.x
!
! Experiment with changing:
!	pgf90 compiler
!	schedule(static,Np/Nthreads)  -> schedule(dynamic,Np/Nthreads) or none
!	Nthreads = 1, 6, 24
!   $omp atomic, $omp  critical updates to Map -> watch the speed drop
!	 
!   dtau = density map of particles. Size: Nr x Nphi.
!   tau  = optical thickness of the disk (map) converted to beta(r,phi)
!   partic = table of particle positions, L, and radial speeds:
!	1=r, 2=phi, 3=beta(tau), 4=tmp, 5=L, 6=v_r=dr/dt
! 
!   Beta = ratio of undiluted stellar radiation to gravity
!   Disk outer radius ~ Rout
!   Np = number of particles
!   freq = frequency of plotting maps, e.g. freq=200 means every 200 timesteps
!   The extinction-calculation grid has size Nr x Nphi. 

 module dataset
	use omp_lib
	implicit none
! constants 
	real, parameter :: Tau_inf = 4.,  Beta = 0.5,   Rout = 2.5
	integer, parameter :: Nthreads = 12, Nj = 6, Mil = 1000000
	integer, parameter :: Nr = 360/12*12, Nphi = Nr
	integer, parameter :: Np = 2 * Mil,	  freq = 200 
	real, parameter    :: pi = atan(1.)*4.,       T_max = 150.   
! arrays and variables
	real :: partic(Nj,Np)  ! particle data: r,phi,vr,L
	real :: dtau(0:Nr-1,0:Nphi-1), tau(0:Nr-1,0:Nphi-1)   ! dtau,tau (r,phi)
	real :: rand_r(2,Np*3)
	real :: rad, c 
	real :: time = 0., dt = 0.005
	integer :: ix, iy, mode, i, j, step

  contains


!
!  This function is ~ #particles per cell (initially)
!______________________________________________________________________
 
 real function Sigma(x)
	real :: x
	real, parameter ::  const = (3. + 1./Rout**4) /Rout
	! n(r) =  4/(3r+1/r**3) has a peak at r=1 
	! Sigma = 4.*x/(3. + 1./(x**4)) or   Sigma = n(r) * r^2
	! Renormalize Sigma to 1 at x=Rout
	Sigma = x/(3. + 1./(x*x*x*x)) * const
	if (x > Rout*0.9) Sigma = 0.
	return
  end

  

!______________________________________________________________________

  subroutine rad_pressure (mode)

	integer :: ir, iphi, mode
! Compute the optical depth from particle positions
! Contribute to map/histogram  dtau, then integrate it along r. 
! In mode=0, compute normalization constant c, giving the disk Tau_inf  
	dtau = 0.
	if(mode==0) c = 1.
!$omp parallel do num_threads(Nthreads) private(ir,iphi)
	do i = 1, Np
		ir   = partic(1,i)/Rout*Nr  
		ir 	 = max(0,min(ir, Nr-1))	
		iphi = max(0,min(int(partic(2,i)/2./pi*Nphi), Nphi-1))	
	
! Histogram update can cause race condition. We diagnose the 
! magnitude of the problem by comparing the total of histogram entries
! with the number of particles thrown in it. If P(race condition)
! is considerable, then we can activate either the critical region
! (guaranteed to be done by single thread) or the atomic update
! (guaranteed non-overlapping writes to memory by threads). 
! In our program, race occurs with P < 0.0004, and we do not have to 
! activate those OpenMP safeguards, since they might slow down the 
! execution of the program. But we find that the slowdown is ~1x (atomic 
! summation) and 30 times (critical region). So we do atomic addition
! and witness no race conditions. 

!///$omp  critical
!$omp atomic 		
	     dtau(ir,iphi) = dtau(ir,iphi) + 1. 
!///$omp end critical 
	end do 

! summarize the accuracy of mapping 
	if(mode==0) print*,'dtau mapping accuracy',sum(dtau)/Np

! integrate optical thickness along radius
	tau(0,:) = 0.
!$omp parallel do num_threads(Nthreads) schedule(static) private(i,j)
	do j = 0, Nphi-1
	 do i = 1, Nr-1
	  tau(i,j) = tau(i-1,j) + c*dtau(i,j)/(i*i)  ! integrate dtau ~ #part c/r^2
	 end do
	end do

! find proper Tau normalization in mode=0 from tau(outer edge)=Tau_inf
	if (mode==0)  then 
		c = Tau_inf * Nphi/sum(tau(Nr-1,:))  ! compute azimuthal aver.
		print*,' mode 0, Tau_inf, c=',Tau_inf,c
		dtau = dtau * c
		tau = tau * c
		print*,' max dtau, tau',maxval(dtau),maxval(tau)
	end if

! convert tau(r,phi) to illumination factor Beta * exp(-tau)	
! pull the resulting illumination value out of the array 
!$omp parallel do num_threads(Nthreads) private(i,ir,iphi)
	do i = 1, Np
		ir   = partic(1,i)/Rout*Nr -1
		ir 	 = max(0,min(ir,Nr-1))	
		iphi = max(0,min(int(partic(2,i)/2./pi*Nphi), Nphi-1))		
		partic(3,i) = Beta * exp(-tau(ir,iphi)) !  beta*exp(-tau)
	end do		
!   print*,' max dtau, tau',maxval(dtau),maxval(tau)
!	print*,' tau at 100',tau(100,0),tau(100,100),tau(100,200)
!	print*,' tau at Nr-1',tau(Nr-1,0:100:28)
!   print*,' max partic(3,:)',maxval(partic(3,:))

  end subroutine rad_pressure


!_____________________________________________________________________

  subroutine initialize()
	integer :: n
	real :: ran,rad
! randomize arrays
	call random_number(rand_r)
	call random_number(partic)
! initialize r, phi
	! try up to 3*Np different r's and reject many
	! in order to produce radial distribution with density Sigma(r)
	n = 0
	do i = 1, 3*Np
		ran = rand_r(1,i)			! random 0..1
		rad = rand_r(2,i) * Rout    ! trial radius, 0..Rout
		if (ran < Sigma(rad)) then  ! accept particle's radius rad
			n = n + 1; 	if (n > Np) exit 	! all r,phi generated
			partic(2,n) = pi*2.*partic(2,n) ! phi = 0...pi*2 
			partic(1,n) = rad			 	! radius 
			if(i < 20) print*,n,'r,phi',rad,partic(2,n)
		end if
	end do
    if (n < Np) stop 'fewer than Np particles' 
! compute tau(r) and radiation pressure force
	print*,'r,phi established, calling rad_press.'
	call rad_pressure(0)
! finish initialization of velocity, based on beta(r).  partic(4,:) = tmp
	partic(4,:) = (1.-partic(3,:))/partic(1,:) ! GM(1-beta(tau))/r 			
	partic(4,:) = sqrt(partic(4,:))            ! v_phi from force 
	partic(4,:) = partic(4,:) *(1.+0.02*(partic(5,:)-0.5)) ! randomize v_phi
	partic(5,:) = partic(4,:)*partic(1,:)     ! store vphi*r = L = const.
	partic(6,:) = 0.01*(partic(6,:)-.5)/sqrt(partic(1,:)) ! vr = +-0.01 vK 
  end subroutine initialize   



!________________________________________________________________________

  subroutine timestep()
	real :: rad(Np), rad2(Np)
	time = time + dt
	rad = partic(1,:)
	rad2 = rad*rad
! evaluate optical thickness, beta = F_rad/F_grav, 
! and the sum of gravity and radiation (accelerations) 
	call rad_pressure (1)
! use partic(4,:) scratch space as grav. acc
	partic(4,:) = (-1.+partic(3,:))/rad2			  		! GM(beta(tau)-1)/r^2 
! evolve particles using angular momentum conservation:  L/r = v_phi
	partic(2,:) = mod(partic(2,:)+dt*partic(5,:)/rad2,2*pi) ! phi+=d_phi
! leapfrog in r direction, 2nd term is centrif. acc. = vphi**2/r
	partic(6,:) = partic(6,:) +dt*(partic(4,:) +(partic(5,:)/rad)**2/rad) ! vr += dvr
	partic(1,:) = partic(1,:) +dt*partic(6,:)			  	! r += vr*dt
  end subroutine timestep


 end module dataset



!======================================================================
! MAIN program
!
 program IRI
	use dataset 
	real (kind=8) :: t
! init
 	call initialize()
	print*,'disk initialized'
! main time loop
  do step = 0, int(T_max/dt)
	t = omp_get_wtime()
	call timestep()	
	t = omp_get_wtime() -t
	if(mod(step,freq)==0) then     ! skip freq timesteps betw. graphs
		print*,'t',time,' st[s]',real(t), partic(1:2,99),partic(6,99)
	    call display()
	end if
  end do 

! after the run
	do i = 1,Np,Np/40
	  print('(7e11.3)'),partic(1:7,i) 
	end do
	print*,'max tau()',maxval(tau)
	print*, tau(398:403, 399)
    print*, tau(398:403, 400) 
    print*, tau(398:403, 401) 
	print*, ' Nr-1',tau(nr_1, 0:Nphi-1:10) 

 end program IRI
!=======================================================================



!______________________________________________________________________
! DISLIN GRAPHICS routine

   subroutine display()
     use dataset 
     use dislin
     real :: arr(Nr,Nphi)
     real :: a0, a1
! prepare normalized array arr ~ surface density ~ (#part/cell)/r ~ r n 
	do i = 1, Nr
		arr(i,:) = dtau(i-1,:)/i   
	end do
	!print*,' min, max dtau',minval(dtau),maxval(dtau)
	arr = 10*alog10(0.01+dtau)
	! arr = arr/(1.+(arr/2)**4)**0.25
	a0 = minval(arr)
	a1 = maxval(arr) 
	print*,' min/max val arr =',a0,a1
	print*,' array slice',arr(100:(Nr-1):(Nr/5),20)
! plot
      !call scrmod('REVERS')
      call metafl('PNG')
      call disini()
      call pagera()
      call hwfont()

      call titlin('Map of particle distribution in (r,phi)',4)
      call titlin('Disk with total optical depth = 4',2)

      call name('10 R ','x')
      call name('Phi ','y')
      call name(' 10 log (surface density)','z')

      call intax()
      call autres(Nr,Nphi)
      call axspos(300,1850)  ! (300,1850)
      call ax3len(1400,1400,1400)  ! (2200,1400,1400)
	  a0 = 1.
! some hard limits on the map plot are given 
      call graf3(0.,25.,0.,5.,0.,2*pi,0.,pi/4,a0,a1,a0,(a1-a0)/4)
      call crvmat(arr,Nr,Nphi,1,1)

      call height(50)
      call title()
      !call mpaepl(3)
      call disfin()
   end subroutine display
!_________________________________________________________________________

