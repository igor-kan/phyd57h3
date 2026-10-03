module mathOps
contains
  attributes(global) subroutine saxpy(x, y, a)
    implicit none
	real (kind=4), parameter :: ADD = 4
    real :: x(:), y(:)
    real, value :: a 
    integer :: i, n
    n = size(x)
    i = blockDim%x * (blockIdx%x - 1) + threadIdx%x
    if (i <= n) y(i) = y(i) +  a*x(i)
  end subroutine saxpy
end module mathOps


program testSaxpy

  use mathOps
  use cudafor
  use omp_lib
  implicit none
  integer, parameter :: N = 300*1024*1024
  real :: x(N), y(N), a
  real, device, allocatable :: x_d(:), y_d(:)
  type(dim3) :: grid, tBlock
  type (cudaEvent) :: startEvent, stopEvent
  real :: time, t_alloc, t_axy, t_send, t_recv, t_cpu
  real (kind=8) :: t0 
  integer :: istat, dev, i

  call system('nvidia-smi')
  tBlock = dim3(512,1,1)
  grid = dim3(ceiling(real(N)/tBlock%x),1,1)


 do dev = 0,1
  istat = cudaSetDevice(dev)
  print*,' device',dev
  t0 = omp_get_wtime()
  allocate (x_d(N),y_d(N))
  t_alloc = omp_get_wtime() - t0
  istat = cudaEventCreate(startEvent)
  istat = cudaEventCreate(stopEvent)

  x = 1.0; y = 2.0; a = 2.0
  t0 = omp_get_wtime()
  x_d = x
  y_d = y
  t_send = omp_get_wtime() - t0
  istat = cudaEventRecord(startEvent, 0)
  t0 = omp_get_wtime()
   call saxpy <<<grid, tblock>>> (x_d, y_d, a)
  t_axy = omp_get_wtime() - t0
  istat = cudaEventRecord(stopEvent, 0)
  istat = cudaEventSynchronize(stopEvent)
  istat = cudaEventElapsedTime(time, startEvent, stopEvent)

  t0 = omp_get_wtime()
  y = y_d
  t_recv = omp_get_wtime() - t0
  print*,'Size:', N/1024/1024, 'M   Max error: ', maxval(abs(y-4.0))
  print*,'GPU a*x+y G(o,B)/s',N*1.e-6/time,N*4.e-6*3/time
  print*,'a*x+y(Gop/s,GB/s):',N*1.e-9*1/t_axy,  N*4.e-9*3/t_axy,  t_axy*1e3,'ms'
  print*,'alloc(Gfl/s,GB/s):',N*1.e-9*2/t_alloc,N*4.e-9*2/t_alloc,t_alloc*1e3,'ms'
  print*,'send (Gfl/s,GB/s):',N*1.e-9*2/t_send, N*4.e-9*2/t_send, t_send*1e3,'ms'
  print*,'recv (Gfl/s,GB/s):',N*1.e-9*1/t_recv, N*4.e-9*1/t_recv, t_recv*1e3,'ms'

  deallocate (x_d,y_d)
  istat = cudaEventDestroy(startEvent)
  istat = cudaEventDestroy(stopEvent)
 end do

!--------CPU
  print*,' device = CPU'
  t0 = omp_get_wtime()
!$omp parallel do 
  do i = 1,N
   y(i) = y(i)+a*x(i)
  end do
!	y = y + a*x
  t_cpu = omp_get_wtime() - t0
  print*,'CPU  (Gfl/s,GB/s):',N*1.e-9*1/t_cpu, N*4.e-9*3/t_cpu, t_cpu*1e3,'ms'

end program testSaxpy
