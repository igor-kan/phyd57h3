# PHYD57 Course Simulation Programs & Code Archive

Archived course code repository from [`https://planets.utsc.utoronto.ca/~pawel/progD57/`](https://planets.utsc.utoronto.ca/~pawel/progD57/).

Contains 99 code and data files implementing numerical physics, numerical methods, parallel computing (CUDA, Fortran, C, Python), and benchmark simulations.

---

## 🗂️ Overview by Topic & Language

### 1. High Performance Computing & GPU (CUDA & Fortran)
- `simple_saxpy_cuda.cu`, `simple_saxpy_cuda-.cu` — Basic CUDA SAXPY kernels and driver code.
- `cuda-perf.f95` — CUDA Fortran GPU performance benchmarks.
- `cudafor-laplace3-dp.f95`, `cudafor-laplace3-sp.f95`, `cudafor-laplace3-new.f95` — 2D Laplace relaxation solvers in CUDA Fortran (single & double precision).
- `ifor-laplace3-dp.f90`, `pgf-laplace3-dp.f95` — CPU Laplace relaxation solvers compiled with Intel `ifort` and PGI/NVIDIA `nvfortran`.
- `callingC-from-py2.py`, `callingC-0-py2.py`, `use_libc.c`, `libfun.c`, `fun_lib.c`, `fun_lib0.c` — Foreign Function Interface (FFI) bindings between C and Python.

### 2. Physical Simulations & Dynamics
- `phys-pendulum.py` — Nonlinear physical pendulum solver.
- `inv-pend-ctrl-3orig+plt.f95`, `inv-pend-ctrl-4a.f95`, `inv-pend-ctrl-4b.f95` — Inverted pendulum control algorithms.
- `broom-ctrl-5.f95`, `broom-ctrl-6.f95` — Broom balancing inverted pendulum dynamics.
- `kepl-GJ-3512b.py` — Exoplanet Keplerian orbit fitting & dynamics.
- `Radioactive.py` — Monte Carlo radioactive decay simulation.
- `dusty-box-1.py` — Dust grain dynamics in a gas box.
- `simpler-nb-0.f90`, `simpler-nb-1.f90` — Gravitational N-body simulation codes.
- `tetraDc.f90`, `tetraDc-3.f90`, `tetraDg-3.f95` — 4-body gravitational tetrahedral choreographies.

### 3. Wave & PDE Solvers
- `pond1.py`, `pond3.py`, `pond4.py` — 2D surface water wave simulation in a shallow basin.
- `pond4-1obj.py`, `pond4-2slits4.py`, `pond4-2slits5.py` — Wave diffraction & double slit wave interference in 2D.
- `interference-1.py` — Wave superposition and interference patterns.
- `laplacian-5t.py` — 5-point discrete Laplacian finite-difference stencil operator.

### 4. Root Finding, Optimization & Quadrature
- `simple_bisec.py` — Bisection root finding.
- `simple_secant.py` — Secant method root finding.
- `simple_newton.py` — Newton-Raphson iteration.
- `compare_sqrt-2.py` — Convergence rates for square root algorithms.
- `integ-p124-*.py` — Numerical numerical integration methods (trapezoidal, Simpson's, Romberg).
- `fit-3par.py`, `fit-4parN.py`, `fit-4parN2.py` — Multi-parameter nonlinear least squares fitting.

### 5. Random Walks & Monte Carlo
- `simple_mtc_pi.py`, `simple_mtc+int_pi.py`, `simple_mtc_pi-4results.py` — Monte Carlo calculation of $\pi$.
- `rnd-walk-gamble-0.py`, `rnd-walk-gambles.py` — Random walk and gambler's ruin simulations.
- `expfract-s1.py`, `expfract-p1.py` — Continued fraction & exponential series evaluations.
- `oxford-IO-2.py`, `oxford-IO-3.py`, `oxford_sunny.dat` — Weather station time-series data analysis.
