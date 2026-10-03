! inv-pend-ctrl-#
! simple NN to learn control of an inverted pendulum (agle phi=0 in the cottom position),
! located on a cart (at coordinate x), via force applied to the cart. 
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
	real(8), parameter :: Tend = 20., dt = 0.002 ! [s] learning time, time-step
	integer, parameter :: Nets = 300e3, Npar = 14, Nneur = 4     
	integer, parameter :: Nsteps = floor(Tend/dt)
	real(8), parameter :: mu = 1./(1.+2.), g_L = 9.81 ! m1/(m1+m2), g/L
	real(8), parameter :: gamm = 0.01		! damping parameter (inverse time)
!  one pendulum, net, and NN 
	real(8) :: pend(6), par(Npar+1), nn(Nneur)
! simplex
	real(8) :: splx(Npar+1,Npar+1), store(Npar+1,Nets) 
!  history of 1 run for plotting
	real(4) :: swing(Nsteps,6+1)
contains


 function phi_tt (x_tt_ext)
	real(8) :: phi_tt, phi_t, phi, x_tt_ext
	phi = pend(1)
!	phi_tt = -(g_L*sin(phi) + x_tt_ext cos(phi) + mu cos(phi)sin(phi) phi_t^2]/ &
!			 (1 - mu cos^2 phi)  -gamm*phi_t    ! for mu > 0
!
	phi_tt = -(g_L*sin(phi) + x_tt_ext*cos(phi)) -gamm*pend(2)	! mu = 0
 end function 


 function sig(x)
! sigmoid function simpler but similar to arctan(x)*(2/pi)
	real(8) :: sig, x
	sig = x/(par(14)+x)  ! |x| > par(14) gets flattened to stay below 1 		
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
	call random_number(par) ! 0..1
	par(1:Npar-1) = par(1:Npar-1) - 0.5
	par(Npar) = 0.5 + 0.5* par(Npar)  ! par(14)=0.5..1, hyper-parameter of the sigmoid 
	par(Npar+1) = 0.  ! reserved for fitness function value
 end subroutine



 subroutine useNN (x_tt_recom)
!
! structure of the net:
!  0      2
!  0   1     4 --> output  
!  0      3
!  0
!  input values are layer 0, they are not normalized by a sigmoid function; 
!  level 1 has 1 neuron, level 2 has 2 neurons, level 3 has 1 neuron
	real(8) :: x_tt_recom
	nn(1) = sig(par(1)*pend(1)+par(2)*pend(2)+par(3)*pend(5)  &
		+ par(4)*pend(6))					! linear comb. of phi,phi_t,x_t,x_tt
	nn(2) = sig(par(5)*pend(1)+par(6)*pend(2)+par(7)*pend(5)) ! phi,phi_t,x_t	 
	nn(3) = sig(par(8)* nn(1) +par(9)*pend(2)) ! +par(10)*nn(5))  ! nn(1),phi_t	 
	nn(4) = sig(par(11)*nn(1) +par(12)*nn(2) +par(13)*nn(3))  ! nn(1),nn(2),nn(3) 	 
	x_tt_recom =  nn(4)     ! allow x_tt_ext up to 1  m/s^2
 end subroutine



 subroutine evolve (fit, iw)
	integer :: istp, iw
	real(8) :: fit, y, x_tt_ext
	real(4) :: pi = atan(1.)*4.
	call setup_pend ()
	fit = 0.d0
	do istp = 1, Nsteps
	  call useNN (x_tt_ext) ! NN recommends to apply x_tt based on pendulum state
	  pend(3) = phi_tt (x_tt_ext)		! phi_tt
	  pend(2) = pend(2) + dt*pend(3)	! phi_t
	  pend(1) = pend(1) + dt*pend(2)	! phi
	  pend(6) = x_tt_ext !-0.* pend(4)	! x_tt, assuming mu=0, add terms otherwise
	  pend(5) = pend(5) + dt*pend(6)	! x_t
	  pend(4) = pend(4) + dt*pend(5)	! x
!	   contribute to fitness function, mainly dependent on <y>
	  if(istp/2*2==istp) y  = -2*cos(pend(1))
	  fit = fit + y		! <-cos(phi)> should be as close to +1 as possible 
	  fit = fit -0.07*(abs(pend(2))+abs(pend(5))) ! penalize |d/dt|'s 
! save data for a plot
	  if(iw) then 
		 swing(istp,1:6) = pend(1:6); swing(istp,7) = istp*dt ! system's state & time
	  end if
! print
	  if(iw) then 
			if(istp/500*500==istp .or. istp > Nsteps-5) print '(i6,7f9.4)',&
			 istp, pend(1:2),pend(4:6),x_tt_ext,fit/istp
	  end if
	end do ! istp
! simulation ended

	fit = fit/Nsteps    ! average 
	fit = fit -0.03*abs(pend(4)) ! also penalize big |x| at the end 
	par(Npar+1) = fit
	if(iw) print*,' fit', fit 
! plot
	if(iw) call plot_3f('XWIN', Nsteps,swing(:,7), & 
		swing(:,1)/pi,swing(:,2)/10.,swing(:,6)/20.)	
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
      CALL AXSLEN(1400,920)
      CALL NAME('time','X')
      CALL NAME('phi, dphi/dt','Y')
      CALL LABDIG(-1,'X')
      CALL TICKS(10,'XY')
!      CALL TITLIN('Plot of phi and dphi/dt',1)  ! <--modify
      CALL TITLIN('phi(t) red, dphi/dt blue, x-accel. green',3)  	! <--modify
! graf(XA, XE, XOR, XSTEP, YA, YE, YOR, YSTEP)
! XA, XE (YA, YE) are the lower and upper limits of the X (Y) axis.
! XOR, XSTEP (YOR,..) are the first X(Y)-axis label and the step between 
	  ymi = min(minval(y1(1:N)),minval(y2(1:N)))*1.2
	  yma = max(maxval(y1(1:N)),maxval(y2(1:N)))*1.2
	  do i = 1,nx
		y3(i) = min(y3(i),yma); 	y3(i) = mAX(y3(i),ymi)
	  end do
      CALL GRAF(0.,x(N),0.,x(N)/5,  ymi,yma,ymi,(yma-ymi)/10.)
      CALL TITLE()
      CALL COLOR('GREEN')
      CALL CURVE(x,y3,N)
      CALL COLOR('RED')
      CALL CURVE(x,y1,N)
      CALL COLOR('BLUE')
      CALL CURVE(x,y2,N)
      CALL COLOR('FORE')
      CALL DASH()
      CALL XAXGIT()
      CALL DISFIN()
	  return
  end subroutine plot_3f      

end module pendulum



!______________________________________________________________________________
!	main program
!______________________________________________________________________________
 
 program pendulum_ctrl
	use pendulum
	use omp_lib
	implicit none
	integer :: j,v
	real(8), save :: f, best_fit, par_best(Npar+1), perturb(Npar)

! store a large number (Nets) of trial nets and their results
	best_fit = -1e20
	do j = 1, Nets
		call setup_net 	 	! with random parameters
		call evolve (f, 0)  ! one pendulum
		store(1:Npar+1,j) = par(1:Npar+1)   ! the last value is fit 
		if(j/5000*5000==j) &
			print '(i7,a,f11.3,a,4f8.3,a)',  j,' fit ',f,' par',par(1:4),'..'
		if (f > best_fit) then 
			v = j;  best_fit = f
		end if
	end do ! j
! the best fit is at v
	par_best = store(1:Npar+1,v)
	par = par_best
	splx(:,Npar+1) = par_best	
	call evolve(f,1)  
	print*,v,' is best, par:',par_best,'=fit'
	print*,' building splx around the par_best'
! build a simplex of Npar+1 vertices
	do j = 1,Npar
	   call random_number(perturb)
	   par(1:Npar) = (1+0.1*(perturb-0.5))*par_best(1:Npar)  ! vary par_best +-0.05
	   call evolve (f,0)  ! among others, puts fit into par(Npar+1)
	   splx(:,j) = par
	end do
! 
	print*,' simplex has been built'
! evolve the simplex 


 end program pendulum_ctrl
