! inv-pend-ctrl-#
!
! simple NN to learn control of an inverted pendulum (angle phi=0 in the bottom 
! position), located on a cart (at coordinate x), via accel. applied to the cart. 
! 
!             O  m1
!              \
!               \
!              |_m2_|
!_______________o__o___________ x
!
!
!  phi_tt = -[g/L sin(phi) +x_tt_ext cos(phi)/L + mu cos(phi)sin(phi) phi_t^2]/
!			 (1 - mu cos^2 phi)
!  x_tt  = x_tt_ext + mu L [sin(phi) phi_t^2 - cos(phi) phi_tt)]
!  where mu  = m1/(m1+m2) < 1, and L = length of the arm. 
!  At first, we assume mu --> 0. 
!

module pendulum 	
	use omp_lib
	implicit none
	integer, parameter :: Nets = 140000, Nneur = 4, Npar = 14    
	real(8), parameter :: Tend = 20., dt = 0.002 ! [s] learning time, time-step
	integer, parameter :: Nsteps = floor(Tend/dt)	! ~1e4
	real(8), parameter :: mu = 1./(1.+2.),  L = 1., g_L = 9.81, pi=atan(1d0)*4d0 
!  mass ratio mu = m1/(m1+m2) is not used at this time
	real(8), parameter :: gamm = 0.01	! damping parameter (inverse time)
!  one pendulum, net, and NN 
	real(8) :: pend(6), par(Npar+1), nn(Nneur)
!  history of 1 run for plotting
	real(4) :: swing(Nsteps,6+1)
!  simplex
	real(8) :: splx(Npar+1,Npar+1), store(Npar+1,Nets) 

contains


! physics of the pendulum:  d^2 phi/ dt^2 = phi_tt (external x-accelertion)
!  
 function phi_tt (x_tt_ext)
	real(8) :: phi, x_tt_ext, phi_tt    
!
! very simple physics: gamm = small rotational friction coeff.
	phi = pend(1)
	phi_tt = -(g_L*sin(phi) + x_tt_ext*cos(phi)) -gamm*pend(2)
!
!  this more complicated physics is not used: pendulum is heavy and 
!  influences the resultant x-acceleration.  
!   mu = mass parameter = m_pend/(mass_pend + mass_platform)
!	phi_tt = -(g_L*sin(phi) +x_tt_ext*cos(phi) +mu*cos(phi)sin(phi)*phi_t^2]/&
!			 (1 - mu*cos^2 phi)  -gamm*phi_t    ! for mu > 0
 end function 



 subroutine setup_pend ()
! initialize the pendulum always the same way
	pend(1) = 2.			! phi 	 [rad] 
	pend(2) = -0.1			! phi_t	 [rad/s] 
	pend(3) = 0. 		 	! phi_tt [s^-2] 
	pend(4) = 0.			! x 	 [m]
	pend(5) = 0.1			! x_t    [m/s]
	pend(6) = 0.			! x_tt   [m/s^2]
 end subroutine

 
 subroutine setup_net ()
!  initialize the net parameters randomly
	call random_number(par)			! 0..1
	par(1:Npar-1) = par(1:Npar-1) - 0.5		! -0.5 ... +0.5
! sigmoid function contains one hyper-parameter, par(Npar)
	par(Npar) = 0.5 + 0.7*par(Npar) ! 0.5..1.2  
	par(Npar+1) = 0.  				! reserved for fitness function value
 end subroutine



 subroutine useNN (x_tt_recom)
!
! structure of the 14-parameter net (+1 hyper-param in sigmoid) 
! the inputs are: phi, phi_t, x_t, x_tt, so it's a recurrent net 
! (previous x_tt affects next x_tt) 
!
!  0 ---- 2
!    \/  /  \
!  0 -- 1 --- 4 --> output
!    / \   \ /
!  0 ------ 3
!    / 
!  0
!  input values are layer 0, they are not normalized by a sigmoid function 
!  level 1 has 1 neuron, level 2 has 2 neurons, level 3 has 1 neuron.
	real(8) :: x_tt_recom
	! nn(1) combines all inputs:  phi,phi_t,x_t,x_tt   (x_tt makes NN recurrent)
!	nn(1) = sig(par(1)*pend(1)+par(2)*pend(2)+par(3)*pend(5)+par(4)*pend(6))
	! phi,phi_t,x,nn(1)
!	nn(2) = sig(par(4)*pend(1)+par(5)*pend(2)+par(6)*pend(4) +par(7)*nn(1))	 
	! nn(1),phi_t,x_t,nn(2)
!	nn(3) = sig(par(8)* nn(1) +par(9)*pend(2) +par(10)*pend(5) +par(11)*nn(2))			
!	nn(4) = sig(par(12)*nn(1) +par(13)*nn(2)  +par(14)*nn(3)) ! nn(1),nn(2),nn(3) 	
!-----------------orig with error
	nn(1) = sig(par(1)*pend(1)+par(2)*pend(2)+par(3)*pend(5)  &
		+ par(4)*pend(6))					! linear comb. of phi,phi_t,x_t,x_tt
	nn(2) = sig(par(5)*pend(1)+par(6)*pend(2)+par(7)*pend(5)) ! phi,phi_t,x_t	 
	nn(3) = sig(par(8)* nn(1) +par(9)*pend(2)) ! +par(10)*nn(5))  ! nn(1),phi_t	 
	nn(4) = sig(par(11)*nn(1) +par(12)*nn(2) +par(13)*nn(3))  ! nn(1),nn(2),nn(3) 
!	 
	x_tt_recom = nn(4)   ! allows  x_tt_ext  up to ~1 m/s^2 ~ 0.1g
 end subroutine



 function sig(x)
! sigmoid function simpler than but similar to arctan(x)*(2/pi)
	real(8) :: sig, x
	sig = x/(par(Npar)+x)  ! |x| > ~par(Npar)  renorms to stay below 1 		
 end function




 subroutine evolve1 (fit, iw, ipl)
! one pendulum experiment with values of parameters in par()
	integer :: st, iw, ipl     ! st=step #, iw,ipl control printing and plotting
	real(8) :: t,y, fit, x_tt_ext, pi = atan(1d0)*4d0, pi2 = atan(1d0)*8d0
!
	call setup_pend ()
	fit = 0.d0
	do st = 1, Nsteps
	  t = st*dt; y = 0.
!  NN recommends to apply x-acceler. x_tt_ext, based on current state of pendulum
	  call useNN (x_tt_ext)  		 ! argument is the output of the subroutine
	  pend(3) = phi_tt (x_tt_ext)	 ! phi_tt = function of pendulum & ext. push
	  pend(2) = pend(2) + dt*pend(3) ! phi_t
	  pend(1) = mod( pend(1) + dt*pend(2), pi2) 	! phi in range 0...2pi
	  pend(6) = x_tt_ext			 ! x_tt(mu=0) 
	  pend(5) = pend(5) + dt*pend(6) ! x_t
	  pend(4) = pend(4) + dt*pend(5) ! x
! contribute to the fitness function, mainly dependent |phi-pi|
	  if(st/2*2==st) y  = -2*cos(pend(1))
	  fit = fit + y		! <-cos(phi)> should be as close to +1 as possible 
	  fit = fit -0.07*(abs(pend(2))+abs(pend(5))) ! penalize |d/dt|'s 	 
!	 df = -abs(pend(1)-pi) !  phi should stay close to pi 
!	  df = df -(0.3*abs(pend(2))+0.5*abs(pend(5))) ! penalize phi & x-speeds
!	  fit = fit + df *min(1d0,t/4d0)  ! time-ramped
! save data for a plot
	  if(ipl) then 
		 swing(st,1:6) = pend;   swing(st,7) = t ! system's state & time
	  end if
! print, every 500th step
	  if(iw .and. (mod(st,500)==0 .or. st > Nsteps-5) ) &
		 print '(f5.1,5f8.3,f9.3)',t,pend(1:2),pend(4:6),x_tt_ext,fit/st
	end do ! st
! simulation ended
	fit = fit/Nsteps    ! average 
	fit = fit -0.03*abs(pend(4)) ! also penalize big |x| at the end 
	par(Npar+1) = fit
	if(iw) print*,' fit', fit 
! plot
	if(ipl) call plot_3f('XWIN',Nsteps, &
		swing(:,7),swing(:,1)/real(pi),swing(:,2),swing(:,4))
 end subroutine


 subroutine evolve (fit, iw, ipl)
	integer :: istp, iw, ipl
	real(8) :: fit, y, x_tt_ext, t, pi2 = atan(1d0)*8d0
	call setup_pend ()
	fit = 0.d0; y = 0.d0
	do istp = 1, Nsteps
	  t = dt*istp
	  call useNN (x_tt_ext) ! NN recommends to apply x_tt based on pendulum state
	  pend(3) = phi_tt (x_tt_ext)		! phi_tt
	  pend(2) = pend(2) + dt*pend(3)	! phi_t
	  ! pend(1) = mod( pend(1) + dt*pend(2), pi2)	! phi
	  pend(1) = pend(1) + dt*pend(2)
	  pend(6) = x_tt_ext !-0.* pend(4)	! x_tt, assuming mu=0, add terms otherwise
	  pend(5) = pend(5) + dt*pend(6)	! x_t
	  pend(4) = pend(4) + dt*pend(5)	! x
!	   contribute to fitness function, mainly dependent on <y>
	  if(istp/2*2==istp) y  = -2*cos(pend(1))
	  fit = fit + y		! <-cos(phi)> should be as close to +1 as possible 
	  fit = fit -0.07*(abs(pend(2))+abs(pend(5))) ! penalize |d/dt|'s 
! save data for a plot
	  if(ipl) then 
		 swing(istp,1:6) = pend(1:6); swing(istp,7) = t ! system's state & time
	  end if
	  if(iw) then 
			if(istp/500*500==istp .or. istp > Nsteps-5) print '(i5,6f8.3,f9.3)',&
			istp,pend(1:2),pend(4:6),x_tt_ext,fit/istp
	  end if
	end do ! istp
! simulation ended
	fit = fit/Nsteps    ! average 
	fit = fit -0.03*abs(pend(4)) ! also penalize big |x| at the end 
	par(Npar+1) = fit
	if(iw) print*,' fit', fit 
! plot
	if(ipl) call plot_3f('XWIN',Nsteps, &
		swing(:,7),swing(:,1)/real(pi),swing(:,2)/5.,swing(:,5)/5.)		 
 end subroutine


!_______________________________________________________________________
!     plot 3 functions with DISLIN
!_______________________________________________________________________
  subroutine plot_3f (CDEV,nx,x,y1,y2,y3)
! allowed plot formats and devices, CDEV = 
!	CONS (Screen, full window),   XWIN (Screen, small window),  
!	GL (OpenGL window),	PS, EPS, PDF, SVG, GIF, TIFF, PNG, PPM, BMP.
      use dislin
      implicit none
      REAL, DIMENSION(*) :: x, y1, y2, y3
	  real :: ymi,yma
      INTEGER :: nx, N, i
	  CHARACTER (LEN=*) :: CDEV     
	  N = nx !  size(x)
	  CALL METAFL(CDEV)
      CALL SETPAG('DA4L')  ! A4 Landscape
      CALL DISINI()
      CALL PAGERA()
      !CALL COMPLX()   ! fonts
      CALL AXSPOS(800,1800)
      CALL AXSLEN(1600,1000)
      CALL NAME('time','X')
      CALL NAME('phi, dphi/dt','Y')
      CALL LABDIG(-1,'X')
      CALL TICKS(10,'XY')
!      CALL TITLIN('Plot of phi and dphi/dt',1)  ! <--modify
      CALL TITLIN('phi (red), dphi/dt (green), dx/dt (blue)',3) ! <--modify
! graf(XA, XE, XOR, XSTEP, YA, YE, YOR, YSTEP)
! XA, XE (YA, YE) are the lower and upper limits of the X (Y) axis.
! XOR, XSTEP (YOR,..) are the first X(Y)-axis label and the step between 
	  ymi = min(minval(y1(1:N)),minval(y2(1:N)))
	  yma = max(maxval(y1(1:N)),maxval(y2(1:N)))
	  do i = 1,nx
		y3(i) = min(y3(i),yma); 	y3(i) = mAX(y3(i),ymi)
	  end do
      CALL GRAF(0.,x(N),0.,x(N)/5,  ymi,yma,ymi,(yma-ymi)/5.)
      CALL TITLE()
      CALL COLOR('RED')
      CALL CURVE(x,y1,N)
      CALL COLOR('GREEN')
      CALL CURVE(x,y2,N)
      CALL COLOR('BLUE')
      CALL CURVE(x,y3,N)
      CALL COLOR('FORE')
      CALL DASH()
      CALL XAXGIT()
      CALL DISFIN()
	  return
  end subroutine plot_3f      


end module pendulum



!_________________________________________________________________________________
!	main program
!_________________________________________________________________________________
 
 program pendulum_ctrl
	use pendulum
	use omp_lib
	implicit none
	integer :: j,v
	real(8), save :: f, best_fit, par_best(Npar+1), perturb(Npar)

! run a large number (Nets) of trial nets and their results
	best_fit = -1e20
	do j = 1, Nets
		call setup_net 	 	! with random parameters
		call evolve (f,0,0) ! one pendulum evolution, no printing or plotting
		store(1:Npar+1,j) = par(1:Npar+1)   ! Npar+1 value: the fitness 
		if (f > best_fit) then 
			v = j;  best_fit = f
		end if
		if(mod(j,5000)==0) print '(i6,a3,e11.3,a5,7f8.3)', &
            j,' f',best_fit,' pend',pend(1:7)
!		if(mod(j,1000)==0) print*,j,' f',f 
	end do ! j
! the best fit is at vertex v 
	par_best = store(1:Npar+1,v)
	par = par_best
	splx(:,Npar+1) = par_best	
	call evolve (f,1,1)		 ! re-run, print and plot the best case  
	print*,v,' is best, par:',par_best,' last=fit'
	print*,' building splx around the par_best'
! build a simplex of Npar+1 vertices
	do j = 1, Npar
	   call random_number(perturb)
	   par(1:Npar) = (1+0.02*(perturb-0.5))*par_best(1:Npar) ! vary par_best+-0.01
	   call evolve (f,0,0)   ! f= fit = par(Npar+1)
	   splx(:,j) = par
	end do
! 
	print*,' simplex has been built'
! evolve the simplex 

 end program pendulum_ctrl
