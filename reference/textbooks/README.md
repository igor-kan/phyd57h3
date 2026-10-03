# PHYD57 Textbooks & References

Comprehensive literature archive downloaded from the course reference pages:
- [`planets.utsc.utoronto.ca/~pawel/PHYD57/tajne/`](https://planets.utsc.utoronto.ca/~pawel/PHYD57/tajne/)
- [`planets.utsc.utoronto.ca/~pawel/PHYD57/tajne/markets/`](https://planets.utsc.utoronto.ca/~pawel/PHYD57/tajne/markets/)
- [`planets.utsc.utoronto.ca/~pawel/PHYD57/refs/`](https://planets.utsc.utoronto.ca/~pawel/PHYD57/refs/)

> **Git Tracking Policy**: Binary PDF files are excluded from git via `.gitignore` to maintain a lightweight repository. All books are preserved locally in the folder structure below.

---

## 📁 Literature Categories & Counts

| Directory | Core Topics | Files |
|-----------|-------------|-------|
| `history-of-computing/` | Pioneers, ILLIAC IV supercomputer, FORTRAN creation | 5 |
| `python/` | Python 3, Scientific Computing, Numerical QM | 6 |
| `linux/` | Shell programming, CentOS/Rocky, Command-line guides | 3 |
| `fortran/` | Fortran 90/95/2008/2018, CUDA Fortran, Intel/PGI compiler user guides | 11 |
| `c-cpp/` | K&R C, C++ Intro, Systems programming | 4 |
| `cuda/` | NVIDIA CUDA C/C++, NVCC compiler driver, GPU architecture | 9 |
| `openmp/` | OpenMP 4.5 specs, multithreaded CPU parallelization tutorials | 2 |
| `numerical-methods/` | Numerical analysis, discretization, linear algebra | 1 |
| `econophysics-ml/` | Neural networks, deep learning, algorithmic trading, financial ML | 55+ |
| `aerodynamics/` | Prandtl boundary layer, lifting line theory, airfoil dynamics | 5 |
| `galactic-dynamics/` | N-body gravitational dynamics, stellar kinematics | 1 |
| `fft/` | Fast Fourier Transform algorithms & NVIDIA CUFFT library | 1 |
| `sph/` | Smoothed Particle Hydrodynamics (SPH) fundamentals | 2 |
| `bridges/` | Suspension and cable-stayed bridge structural mathematics | 2 |

---

## 📚 Detailed Bibliography

### 1. History of Modern Computing
- `Ceruzzi-History_of_Modern_Computing.pdf` — Ceruzzi: *A History of Modern Computing* (2013).
- `Haigh-New_History_Modern_Comput-2021.pdf` — Haigh & Ceruzzi: *A New History of Modern Computing* (2021).
- `Backus-History_of_Fortran_I,II,III.pdf` — Backus: *The History of FORTRAN I, II, and III* (1978).
- `Hord-Illiac_IV-1st-supercomp-1982.pdf` — Hord: *Illiac IV: The First Supercomputer* (1982).
- `Burroughs.ILLIAC-IV-1974.pdf` — Burroughs Corp.: *ILLIAC IV Systems Characteristics* (1974).

### 2. Python & Scientific Computing
- `Schoerghofer-Lessons.pdf` — Schörghofer: *Lessons in Scientific Computing*.
- `Linge-Programming_for_Computations.pdf` — Linge & Langtangen: *Programming for Computations - Python 3*.
- `Turner-Applied_Sci_Computing_Python-.pdf` — Turner et al.: *Applied Scientific Computing with Python*.
- `Izaac-Computational_QM-2019.pdf` — Izaac & Wang: *Computational Quantum Mechanics* (2019).
- `Shaw-Learn_Python3_the_Hard_Way-2017.pdf` — Zed Shaw: *Learn Python 3 the Hard Way* (2017).
- `Shaw-Learn_More_Python3_the_Hard_Way-2017.pdf` — Zed Shaw: *Learn More Python 3 the Hard Way* (2017).

### 3. Linux & System Architecture
- `Gedris-Intro_Linux_Command_Shell_for_Beginners-2003.pdf` — Gedris: *Introduction to Linux Command Shell*.
- `Matthew,Stones-Beginning_Linux_Programming-2008.pdf` — Matthew & Stones: *Beginning Linux Programming*.
- `Sobell-A_practical_Guide_to_Linux_Commands-2018.pdf` — Sobell: *A Practical Guide to Linux Commands, Editors, and Shell Programming*.

### 4. Fortran & CUDA Fortran
- `Chivers-Intro_to_Prog_w_Fortran-4ed-2018.pdf` — Chivers & Sleightholme: *Introduction to Programming with Fortran* (4th ed.).
- `Chapman-Fortran_for_Scientists_and_Engineers-2018.pdf` — Chapman: *Fortran for Scientists and Engineers* (4th ed.).
- `Ray-Fortran_2018_With_Parallel_Programming-2020.pdf` — Subrata Ray: *Fortran 2018 with Parallel Programming*.
- `Brainerd-Guide_to_Fortran_2008_Programing-2015.pdf` — Brainerd: *Guide to Fortran 2008 Programming*.
- `Fatica,Ruetsch-CUDA_Fortran_for_Sci_and_Eng-2014.pdf` — Fatica & Ruetsch: *CUDA Fortran for Scientists and Engineers*.
- `CUDA_Fortran_paper.pdf` — Comparative study of CUDA Fortran vs. C vs. CPU performance.
- `ifort-ug+ref.pdf` — Intel Fortran Compiler 16.0 User and Reference Guide.
- `Intel_Fortran_Comp_16.0_User,Ref_Guide.pdf` — Intel Fortran Reference manual (alternate edition).
- `pgi18fortref.pdf` — PGI Fortran Reference (ver. 18).
- `pgi18ug-x86.pdf` — PGI x86 Compiler User Guide.
- `pgi18cudaforug.pdf` — PGI CUDA Fortran Programming Guide and User Reference.

### 5. C & C++
- `Kernighan,Ritchie-Ansi_C_Programming.pdf` — Kernighan & Ritchie: *The C Programming Language* (ANSI C, 2nd ed.).
- `Deitel-C_How_to_Program.Intro_C++_2016.pdf` — Deitel & Deitel: *C How to Program with an Introduction to C++*.
- `Kochan-Programming_in_C.A_Complete_Intro-2004.pdf` — Kochan: *Programming in C: A Complete Introduction*.
- `Shaw-Learn_C_the_Hard_Way-2015.pdf` — Zed Shaw: *Learn C the Hard Way*.

### 6. CUDA C/C++ (GPU Acceleration)
- `CUDA_C_Programming_Guide-2019.pdf` — NVIDIA: *CUDA C Programming Guide*.
- `CUDA_C_Best_Practices-2019.pdf` — NVIDIA: *CUDA C Best Practices Guide*.
- `CUDA_Compiler_Driver_NVCC.pdf` — NVIDIA: *CUDA Compiler Driver NVCC Reference Guide*.
- `Cook-CUDA_programming.pdf` — Shane Cook: *CUDA Programming: A Developer's Guide to Efficient Parallel Computing*.
- `Han-Learn_CUDA-2019.pdf` — Jaegeun Han: *Learn CUDA Programming: A Beginner's Guide*.
- `Storti-CUDA_for_Engineers-2016.pdf` — Storti & Yurtoglu: *CUDA for Engineers: An Introduction to High-Performance Parallel Computing*.
- `Sanders-CUDA_by_Example-2010.pdf` — Jason Sanders & Edward Kandrot: *CUDA by Example*.
- `Wilt-The_CUDA_Handbook-2013.pdf` — Nicholas Wilt: *The CUDA Handbook: A Comprehensive Guide to GPU Programming*.
- `Farber-CUDA_Applications.pdf` — Rob Farber: *CUDA Application Design and Development*.

### 7. Numerical Methods & Mathematics
- `Kincaid-Num_Analysis-2002.pdf` — Kincaid & Cheney: *Numerical Analysis: Mathematics of Scientific Computing* (3rd ed.).

### 8. Aerodynamics & Wing Theory (TU-154M Investigation)
- `Prandtl-Fundam_of_Hydro-and_Aeromechanics.pdf` — Ludwig Prandtl & O. G. Tietjens: *Fundamentals of Hydro- and Aeromechanics*.
- `Prandtl-Applic_modern_hydrodyn_to_aeronautics.pdf` — Ludwig Prandtl: *Applications of Modern Hydrodynamics to Aeronautics*.
- `Oertel-Prandtls_Essent_Fluids_Mech-2004.pdf` — H. Oertel: *Prandtl's Essentials of Fluid Mechanics*.
- `Pope-Basic_Wing_and_Airfoil_Theory-1951.pdf` — Alan Pope: *Basic Wing and Airfoil Theory*.
- `Katz,Plotkin-Low-Speed-Aero-2001.pdf` — Katz & Plotkin: *Low-Speed Aerodynamics: From Wing Theory to Panel Methods*.

### 9. Astrophysics, SPH & Dynamics
- `Binney,Tremaine-Galactic_Dynamics,2ed-2008.pdf` — Binney & Tremaine: *Galactic Dynamics* (2nd ed.).
- `monaghan-sph2005.pdf` — J. J. Monaghan: *Smoothed Particle Hydrodynamics* (Rep. Prog. Phys., 2005).
- `SPH-monaghan1997.pdf` — J. J. Monaghan: *SPH and its Applications to Problems in Astronomy* (1997).

### 10. Signal Processing & Bridges
- `Brigham-The-fast-Fourier-transform-and-its-app-1988.pdf` — E. Oran Brigham: *The Fast Fourier Transform and its Applications*.
- `Gimsing-Cable_Supported_Bridges.pdf` — Gimsing: *Cable Supported Bridges: Concept and Design*.
- `Gazzola-Math_Models_for_Suspension_Bridges.pdf` — Gazzola: *Mathematical Models for Suspension Bridges*.

### 11. Econophysics, Machine Learning & Quantitative Trading
- Complete library of 55+ volumes from `tajne/markets/` covering:
  - Deep Learning & Neural Network Architectures (Aggarwal, Bengio, Cartwright, Hagan, Downing)
  - Quantitative Finance & Asset Pricing (Wilmott, Schmidt, Seydel, Cornuéjols, Gilli, Dempster)
  - Algorithmic & High-Frequency Trading (Cartea, Aldridge, Kissell, Halls-Moore, Mak)
  - Financial Machine Learning (Marcos López de Prado: *Advances in Financial Machine Learning*, *Machine Learning for Asset Managers*)
  - Time Series, Wavelets & Econophysics (Alexandridis, Pal, Jovanovic, Ziemann, Vrbka)
