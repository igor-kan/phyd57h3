> From: https://gemini.google.com/app/d5fdbfc39d798c48

# you asked

message time: 2026-10-03 14:54:40

https://planets.utsc.utoronto.ca/~pawel/PHYD57/ 


1	Structure and scope of the course
	Syllabus of PHYD57
	Numerical Comp. in Physical Sciences: History and Contemporary efforts
	
2	HPC: need for speed, why and how
	History and modernity: microprocessors, Unix, Linux, and Internet
	Intro to Linux (CentOS)
	Command line interface and shells (bash and tcsh)
	Text editors: vi, nano, gedit, micro

3	Connectivity (ssh & sftp, traceroute & ping)
	Securing the linux system against break-ins via /etc/hosts.deny
	Basic Linux shells and commands (bash, tcsh, cd, ls, ps, cd, &, bg, fg, 
	   alias, export/setenv, rm, output redirection to file via >)
	Getting more info: manual pages (man), -h, --help, or -help modifiers
	Recommended compilers:  GNU: gcc, gfortran; Intel: icc, ifort or ifx; 
       		Nvidia: nvcc/nvc++, nvfortran (formerly pgf95) 
	Simple program in C, Fortran95, Python, Matlab, IDL (Schoerghofer,p.30)
	More complex program, example of HPC:
		2nd order Laplace operator stencil for the diffusion equation
	Speed comparison of C/F95 with Python & Numpy: why we learn HPC

4	C and Fortran 95 - compilers, basic usage  
	Numerical puzzle of 711 - learning C and Fortran
	Kruskal counts and their connection to linked lists
	Coding Kruskal counts trick in Python and Fortran 
	C: Language overview, compilers
	Integration with Python: calling C from Python
	Examples of programs
		
5	Dicussion of the solutions of A2 assignment set 
	More Fortran. Monte Carlo method (MtC)
	Examples of programs: Random numbers and MtC (finding π)
	Slow convergence: const./sqrt(N) scaling of error in MtC
	Parallel execution on CPU using OpenMP fork-join method in loops
 	Parallel implementations: in-depth diffusion equation 

6	Modern computing in the era of Integrated Circuits
	2000s: Appearence of barriers to single-thread computing
	The only solution: parallelism 
	Moore's law: sustainable or not? also look at the website in details, its subpages etc.

---

# gemini response

The course portal for **PHYD57 (Advanced Computational Methods in Physics)** hosted at `planets.utsc.utoronto.ca/~pawel/PHYD57/` serves as the primary centralized hub for lecture syllabi, computing cluster access rules, reading references, and project descriptions curated by Prof. Pawel Artymowicz.

---

### 1. Website Architecture and Subpage Resources

The course site operates as an unstyled, direct academic directory containing links to syllabi, project documentation, external texts, and hidden resource pages:

*   **Central Course Hub (`/PHYD57/`):** Contains the official syllabus text file, lecture schedule, language policies, assignment submission criteria, and midterm/final examination rules.
*   **PHYD57 References Page (`References` subpage):** Hosts recommended readings and technical PDFs covering core languages and computing history:
    *   *Lessons in Scientific Computing* by Norbert Schörghofer (specifically pages 25–35 detailing runtime benchmarks between C, Modern Fortran, and Python).
    *   *Computational Quantum Mechanics* by J. Izaac and J. B. Wang (Chapter 2 for Modern Fortran syntax and Chapter 3 for scientific Python).
    *   *The Definitive Guide to CentOS* by Membrey (Chapter 3, covering headless server setups and remote access).
    *   *A History of Modern Computing* by Paul E. Ceruzzi.
    *   *Programming for Computations – Python* by Svein Linge and Aslak Tveito.
*   **Project Dossiers and Hidden Subdirectories:**
    *   **Aerodynamics & Flight Dynamics (`/~pawel/s/`):** A hidden directory (accessed by replacing `PHYD57` with `s` in the URL) dedicated to the Smolensk Tu-154 crash aerodynamic reconstruction, Prandtl lifting-line theory, and 3D vortex panel methods.
    *   **Smoothed Particle Hydrodynamics (SPH):** Papers by J. J. Monaghan (1997, 2005) and Stephan Rosswog (*Astrophysical SPH*) covering Lagrangian fluid modeling.
    *   **N-Body and Galactic Dynamics:** Dynamics references based on Binney & Tremaine’s *Galactic Dynamics*, alongside CUDA N-body integration engines.
    *   **Fast Fourier Transforms (FFT):** Reference texts by E. Oran Brigham and NVIDIA’s `CUFFT_Library.pdf` documentation for solving Poisson and gravitational potential convolutions in $\mathcal{O}(N \ln N)$ time.
    *   **Structural Mechanics (Golden Gate Project):** Suspension bridge modeling based on Gimsing (*Cable Supported Bridges*) and Gazzola (*Mathematical Models for Suspension Bridges*).

---

### 2. Full 12-Week Course Curriculum

The lecture and tutorial track advances from POSIX command-line mechanics to multi-core threading and massively parallel GPU acceleration:

| Week | Lecture Topics | Practical & Computational Focus |
| :--- | :--- | :--- |
| **1** | Course Scope & History of Numerical Computing | Overview of physical simulation paradigms and course logistics. |
| **2** | Microprocessor Evolution & Unix/Linux Essentials | CentOS environment, bash/tcsh shells, and terminal text editors (`vi`, `nano`, `gedit`, `micro`). |
| **3** | Networking & Low-Level Language Benchmarking | SSH/SFTP, `/etc/hosts.deny` security, GNU/Intel/NVIDIA compiler toolchains, 2nd-order Laplace diffusion stencils, and C/Fortran vs. Python/NumPy execution speed comparisons. |
| **4** | C & Modern Fortran 95 Implementations | Compiler optimization flags, the Numerical Puzzle of 711, Kruskal counts, linked list mechanics, and calling C routines from Python. |
| **5** | Monte Carlo Integration & Early OpenMP | Pseudo-random number generators, calculating $\pi$, $\mathcal{O}(N^{-1/2})$ statistical error convergence, OpenMP fork-join loops, and parallelizing the 2D heat diffusion equation. |
| **6** | Integrated Circuit Scaling & Hardware Limits | Dennard scaling breakdown, single-thread performance walls, multi-core chip architectures, and the sustainability of Moore's Law. |
| **7** | Many-Core Architectures & Memory Models | Introduction to group project (A4) options, Intel Many Integrated Core (MIC / Xeon Phi), supercomputing clusters, and row-major (C) vs. column-major (Fortran) array ordering. |
| **8** | Advanced OpenMP & Single-Node Bottlenecks | Stack overflow segmentation faults, CPU compute vs. RAM bandwidth constraints, DISLIN graphics library, wave equations, linked-list neighbor searches, and SPH implementations. |
| **9** | Vectorization, MIC & Introduction to CUDA | Compiler auto-vectorization reports, optically thick disk radiation (IRI), N-body gravitational integration, and simple neural net stabilization (inverted pendulum problem). |
| **10** | Astrophysical Disks, Hydrodynamics & FFT | Protoplanetary disk simulations, Eulerian vs. Lagrangian fluids (`fluidsGL`), gravitational potentials via FFT convolutions, zero-padding/aliasing, and CUDA Fortran kernels. |
| **11** | Massively Parallel CUDA & Machine Learning | CUDA C/C++ thread hierarchies, tetrahedrons puzzle, intro to MPI, neural network dimensionality, overfitting, and the Nelder–Mead Simplex optimization algorithm. |
| **12** | Research Project Capstone | In-class presentations and evaluations of student A4 group research projects. |

---

### 3. Computing Architecture and Toolchains

The course centers on direct access to departmental research clusters housed in the Science Wing and BV Building at UTSC:

*   **Cluster Environments:**
    *   `art-1` and `art-2`: Multi-core servers running CentOS 6 with `tcsh` as the default shell. Users authenticate over legacy SSH ciphers (`-o HostKeyAlgorithms=+ssh-dss`).
    *   `art-16`: Modern GPU accelerator nodes running Rocky Linux 9 with modern `bash`.
    *   `phi`: Multi-core compute nodes equipped with Intel Xeon Phi (Many Integrated Core / MIC) co-processors.
*   **Compiler Suites:**
    *   **GNU Compiler Collection (GCC):** `gcc`, `g++`, and `gfortran`.
    *   **NVIDIA HPC SDK:** `nvcc`, `nvc`, `nvc++`, and `nvfortran` (modern replacement for PGI `pgf90`/`pgf95`).
    *   **Intel oneAPI:** `icx`, `icpx`, and `ifx` (modern replacement for legacy `icc` and `ifort`).
*   **Language Policy:**
    *   *Passive Requirement:* Mandatory ability to read, trace, and debug both C and Modern Fortran (90/95/2003/2008) in lecture codes and exams.
    *   *Active Requirement:* Students select either C/C++ or Modern Fortran as their primary language for homework and exams.
    *   *Python:* Restricted to an auxiliary role (prototyping, driver scripts, plotting data with Matplotlib, and testing numerical accuracy) rather than writing inner simulation kernels.

---

### 4. Course Deliverables and Grading Scheme

Term evaluations balance numerical physics problem sets, multi-threaded coding assignments, and in-person exams:

| Deliverable | Weight | Key Deadlines & Structural Parameters |
| :--- | :--- | :--- |
| **Assignment 1 (A1)** | **7%** | Due at 11:00 AM on Lecture 4. Covers flight mechanics, air-water ballistics, $\mathcal{O}(N)$ optimization, and 2nd-derivative stencil truncation error. |
| **Assignment 2 (A2)** | **7%** | Due at 11:00 AM on Lecture 6. Centers on Monte Carlo simulations, convergence rates, and initial OpenMP loop parallelization. |
| **Midterm Exam** | **16%** | Held in-class during Lecture 7 (11:10–12:10 AM). Split evenly: 8% written problem solving and 8% theoretical quiz. |
| **Assignment 3 (A3)** | **7%** | Due at 11:00 AM on Lecture 10. Focuses on advanced OpenMP, FFT convolutions, and initial CUDA GPU kernel development. |
| **Group Project (A4)** | **23%** | Groups finalized by Lecture 6; project presentations during Lecture 12. Involves developing an end-to-end HPC simulation (SPH fluids, N-body dynamics, aerodynamics, or bridge oscillations). |
| **Final Exam** | **40%** | In-person 3-hour examination split into two sections: ~1.5 hours closed-book written theory and quiz, followed by ~1.5 hours of live coding on a personal laptop or via remote SSH to the `art` cluster. Students may bring up to 8 handwritten note pages (4 double-sided sheets). |

*Submission Policy:* Work submitted more than 3 hours past the 11:00 AM deadline receives an automatic 50% deduction, with no extensions granted due to in-class solution discussions during tutorials. Academic illness accommodations require an official Verification of Illness (VOI) form or ACORN self-declaration.

---

# you asked

message time: 2026-10-03 14:56:57

what chapters/sectiosn i need to read from suggested or other soruces textbooks or onlie to prepare for midterm, and cover material needed to get a1, a2 assignmetns done

---

# gemini response

To successfully complete **Assignment 1 (A1)**, **Assignment 2 (A2)**, and pass both the written problem-solving and theoretical quiz portions of the **Midterm Exam** (Lectures 1–6), your reading must cover three integrated areas: **analytical and numerical physics modeling**, **low-level systems and memory architectures (C & Modern Fortran)**, and **parallel execution (OpenMP)**.

---

### Part 1: Readings for Assignment 1 (A1)
*Due Lecture 4; covers flight dynamics, multiphase ballistics, algorithmic complexity, and finite-difference error scaling.*

#### Problem 1.1: F-16 Aerobatic Loop Analysis
*   **John D. Anderson — *Introduction to Flight* (8th/9th Ed.)**
    *   **Chapter 5 (§5.13–§5.15): Accelerated Flight & Pull-up Maneuvers:** Derives normal load factor $n = 1 + v^2/(gR)$, centripetal pull-up force balance, and apex weightlessness yielding the circular radius relation $R = v_0^2/(5g)$.
    *   **Chapter 5 (§5.16): The $V\text{–}n$ Flight Envelope:** Explains structural load limits and dynamic stall speed scaling $v_S(n) = v_{S,0}\sqrt{n}$.
*   **Bernard Etkin & Lloyd Duff Reid — *Dynamics of Flight: Stability and Control* (3rd Ed.)**
    *   **Chapter 5 (§5.1–§5.6): Vertical-Plane Trajectory Dynamics:** Formulates the coupled longitudinal equations of motion in speed $v(t)$ and flight-path angle $\theta(t)$ under quadratic drag and load-dependent induced drag ($C_D = C_{D0} + K C_L^2$).
*   **William H. Press et al. — *Numerical Recipes: The Art of Scientific Computing* (3rd Ed.)**
    *   **Chapter 16 (§16.1–§16.3): Runge–Kutta & Adaptive Step-Size Control:** Explains how to integrate non-linear coupled ODEs with explicit loop closure checks at $\theta = 2\pi$.
*   **Robert Resnick, David Halliday, & Kenneth S. Krane — *Physics, Vol. 1* (5th Ed.)**
    *   **Chapter 4 (§4.5) & Chapters 7–8:** Airspeed vector triangles under wind shear and mechanical work-energy conservation ($v(y) = \sqrt{v_0^2 - 2gy}$).
*   **Vladimir Arnold — *Mathematical Methods of Classical Mechanics* (2nd Ed.)** *(Advanced/Trans-Syllabus)*
    *   **Chapter 3 (§12, §16):** Clothoid (Euler spiral) curvature parameterization ($\kappa(s) = s/A^2$) to eliminate unbounded normal jerk ($\dot{n} \to \infty$).

#### Problem 1.2: Multiphase Air-Water Ballistics
*   **John R. Taylor — *Classical Mechanics***
    *   **Chapter 2 (§2.1–§2.4): Motion in Resisting Media:** Formulates 1D/2D quadratic aerodynamic drag ($\mathbf{F}_D = -\frac{1}{2}\rho C_D A v \mathbf{v}$) and closed-form vertical terminal velocity $v_t = \sqrt{2m g_{\text{eff}} / (\rho C_D A)}$.
*   **Resnick, Halliday, & Krane — *Physics, Vol. 1* (5th Ed.)**
    *   **Chapter 15 (§15.1–§15.4): Fluid Statics & Buoyancy:** Derives Archimedes’ principle and effective gravitational acceleration in water: $g_{\text{eff}} = g(1 - \rho_w/\rho_p)$.
*   **Randall J. LeVeque — *Finite Difference Methods for Ordinary and Partial Differential Equations***
    *   **Chapters 1–3: Initial Value Problems & Discontinuous Interfaces:** Staggered time-stepping across discontinuous media boundaries (the $\sim 800\times$ density jump at $y=0$).
*   **Press et al. — *Numerical Recipes* (3rd Ed.)**
    *   **Chapter 9 & Chapter 16 (§16.6): Root Finding & Stiff Systems:** Brent’s method for zero-crossing detection to pinpoint the air-water impact time $t^*$ without step-overs, along with handling stiff deceleration spikes.

#### Problem 1.3: Vector Monotonicity & Subsegment Growth
*   **Thomas H. Cormen et al. (CLRS) — *Introduction to Algorithms* (3rd/4th Ed.)**
    *   **Chapter 3 (§3.1–§3.2) & Chapter 4 (§4.1): Asymptotic Growth & Maximum Subarray:** Formal algebraic proofs comparing naive pairwise $\sum_{i=1}^{N-1}(N-i) = \frac{N(N-1)}{2} \in \Theta(N^2)$ against single-pass $\Theta(N)$ running-minimum scans with $\mathcal{O}(1)$ storage.
*   **Randal E. Bryant & David R. O'Hallaron — *Computer Systems: A Programmer's Perspective (CS:APP)* (3rd Ed.)**
    *   **Chapter 5: Optimizing Program Performance:** Instruction-level parallelism (ILP), unrolling loops, branch predictability, and eliminating memory stalls.
    *   **Chapter 6: The Memory Hierarchy:** 64-byte L1/L2/L3 cache lines, spatial/temporal locality, and avoiding strided cache thrashing during multi-million-element traversals.

#### Problem 1.4: Second-Derivative Stencil Limits
*   **Randall J. LeVeque — *Finite Difference Methods for Ordinary and Partial Differential Equations***
    *   **Chapter 1 (§1.1–§1.3): Truncation Error & Taylor Series:** Deriving the second-order truncation error bound ($E_{\text{trunc}} = \frac{h^2}{12}|f^{(4)}(\xi)|$) for the 3-point central difference stencil.
*   **Mark Newman — *Computational Physics***
    *   **Chapter 5 (§5.10): Numerical Derivatives & Roundoff Error:** Analytical derivation of catastrophic subtractive cancellation ($E_{\text{round}} = 4\epsilon_{\text{mach}}|f| / h^2$), proving the optimal step size minimizes at $h_{\text{opt}} \sim \epsilon_{\text{mach}}^{1/4}$, and plotting the log-log error V-curve.
*   **Schörghofer — *Lessons in Scientific Computing* (CRC 2019)**
    *   **Chapter 1 (pp. 25–35):** Benchmarking compiled C/Fortran stencils against Python/NumPy.

---

### Part 2: Readings for Assignment 2 (A2)
*Due Lecture 6; covers Monte Carlo methods, PRNGs, $1/\sqrt{N}$ error convergence, and OpenMP multi-threading.*

#### Monte Carlo Integration & Random Number Generation
*   **Mark Newman — *Computational Physics***
    *   **Chapter 10 (§10.1–§10.3): Random Numbers & Monte Carlo Integration:**
        *   *§10.1:* Linear congruential generators (LCGs), pseudo-random sequences, seeds, and uniform distribution sampling.
        *   *§10.2:* Monte Carlo evaluation of definite integrals (e.g., finding $\pi$ via circle-in-a-square hit-or-miss and mean-value integration).
        *   *§10.3:* Statistical errors and the Central Limit Theorem: rigorous proof of the slow $\sigma \propto \frac{1}{\sqrt{N}}$ error scaling law independent of spatial dimensionality.
*   **Press et al. — *Numerical Recipes* (3rd Ed.)**
    *   **Chapter 7 (§7.1–§7.3): Random Numbers:** Uniform random deviates, period lengths, avoiding defective LCG artifacts (Marsaglia planes).
    *   **Chapter 15 (§15.1): Modeling of Data:** Statistical variance, sample standard deviations, and confidence intervals for stochastic physical simulations.

#### OpenMP Loop Parallelization & 2D Diffusion
*   **Georg Hager & Gerhard Wellein — *Introduction to High Performance Computing for Scientists and Engineers***
    *   **Chapter 6: Shared-Memory Parallel Programming with OpenMP:**
        *   *§6.1–§6.2:* The fork-join thread execution model, parallel regions, and work-sharing loops (`#pragma omp parallel for` in C, `!$omp parallel do` in Fortran).
        *   *§6.3:* Data scoping rules: distinguishing `shared` memory arrays from loop-private variables (`private`, `firstprivate`), thread safety, and preventing data races.
        *   *§6.4:* Reduction clauses (`reduction(+:sum)`): how multi-threaded Monte Carlo loops accumulate partial sums across cores without mutex lock contention.
*   **Milan Curcic — *Modern Fortran: Building Efficient Parallel Applications***
    *   **Chapter 11 & 12: Parallelism with OpenMP & Hardware Vectors:** Implementing OpenMP directives over multidimensional Fortran arrays and understanding loop chunk scheduling (`schedule(static)` vs `schedule(dynamic)`).
*   **LeVeque — *Finite Difference Methods***
    *   **Chapter 9: Diffusion Equations & Parabolic PDEs:** Setting up the explicit 2D 5-point Laplace stencil:
        $$u_{i,j}^{n+1} = u_{i,j}^n + \Delta t \left( \frac{u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n}{\Delta x^2} + \frac{u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2} \right)$$
        Parallelizing grid update loops with OpenMP, managing inner vs. boundary points, and verifying the CFL stability criterion ($\Delta t \le \frac{\Delta x^2}{4D}$).

---

### Part 3: Readings for the Midterm Exam
*Held in Lecture 7; 16% of total grade (8% written problem solving + 8% multiple-choice/fill-in-the-blank quiz). Allowed aid: 8 handwritten note pages (4 double-sided sheets) and a calculator.*

#### A. Microprocessor History, Hardware Architecture & Physical Limits (Quiz Scope)
*   **Paul E. Ceruzzi — *A History of Modern Computing* (2nd Ed.)**
    *   **Chapters 5 & 6:** Transition from mainframes to microprocessors, Intel x86 architecture evolution, Unix/Linux origins, and the rise of the Internet.
*   **Hager & Wellein — *Introduction to High Performance Computing***
    *   **Chapter 1: Modern Processors:** Pipelining, superscalar execution, clock frequency limits, and SIMD registers.
    *   **Chapter 2 (§2.1–§2.3): Memory Hierarchies & Bottlenecks:** Memory wall, arithmetic intensity (FLOPs per byte of DRAM transfer), and L1/L2/L3 cache latency vs. main memory bandwidth.
    *   **Chapter 3: Parallel Computers:** Dennard scaling breakdown (leakage currents and the thermal "power wall" around 2004–2005), multi-core CPUs as the only path forward, and the operational meaning of Moore's Law (transistor count scaling vs. single-thread frequency stagnation).

#### B. Linux CLI, Networking & System Security (Quiz Scope)
*   **Scott Membrey — *The Definitive Guide to CentOS***
    *   **Chapter 3: Working with the Shell & Remote Systems:**
        *   Bash vs. tcsh shell environments, environment variables (`export` vs. `setenv`), aliases, process management (`ps`, `&`, `bg`, `fg`, `kill`), and stream redirection (`>`, `>>`, `|`).
        *   Remote connectivity tools: `ssh` and `sftp` port mechanics, `ping`, `traceroute`, and MTU limits.
        *   Security mechanisms: Securing access through `/etc/hosts.deny` and `/etc/hosts.allow` TCP wrappers.
        *   Text editor fluency: Command modes in `vi`, basic usage of `nano` and `micro`.

#### C. Language Mechanics, Memory Models & Compiler Suites (Quiz & Written Scope)
*   **Norbert Schörghofer — *Lessons in Scientific Computing***
    *   **Chapter 1 (§1.1–§1.4, pp. 1–35): Languages & Computational Trade-offs:** Language performance taxonomy (C, Fortran 95, Python, NumPy, MATLAB, IDL); how interpreted dynamic typing incurs massive loop interpretation penalties compared to compiled binaries.
*   **J. Izaac & J. B. Wang — *Computational Quantum Mechanics***
    *   **Chapter 2 (pp. 35–75): Modern Fortran Foundations:** Module design, strict typing (`implicit none`), array slices (`A(1:N:2)`), dynamic allocation (`allocate`/`deallocate`), and intrinsic math functions.
    *   **Chapter 3 (pp. 77–110): Scientific Python:** NumPy vectorized arrays, SciPy libraries, and calling compiled C/Fortran libraries via Python wrappers (`ctypes`, `f2py`).
*   **K. N. King — *C Programming: A Modern Approach* (2nd Ed.)**
    *   **Chapters 11, 12, & 17: Pointers, Arrays, and Dynamic Memory:**
        *   Pointer arithmetic and array memory layout: C row-major (lexicographical) order versus Fortran column-major order.
        *   1D flattened contiguous buffers (`grid[i * N + j]`) versus jagged pointer arrays (`grid[i][j]`), and why jagged arrays destroy cache locality.
*   **Compiler Manuals & Optimization Flags (GCC, Intel, NVIDIA SDK):**
    *   GNU (`gcc`, `gfortran`), Intel (`icc`, `ifort`, `ifx`), and NVIDIA (`nvcc`, `nvfortran` / formerly PGI `pgf95`).
    *   Optimization flags: `-O2`, `-O3`, `-march=native`, loop unrolling, and `-fopenmp` / `-qopenmp`.

#### D. Algorithmic Puzzles & Problem-Solving (Written & Quiz Scope)
*   **The Numerical Puzzle of 711 (Lecture 4):**
    *   *Concept:* Four items whose sum is $\$7.11$ and product is $\$7.11$ (in cents: $a+b+c+d=711$ and $a \cdot b \cdot c \cdot d = 711,000,000$).
    *   *Focus:* Prime factorization of $711 \times 10^6 = 2^6 \cdot 3^2 \cdot 5^6 \cdot 79$. Understand analytical constraint pruning (isolating multiples of 79, ordering $a \le b \le c \le d$) to turn a brute-force $711^4 \approx 2.5 \times 10^{11}$ loop into an efficient multi-loop running in milliseconds in C/Fortran.
*   **Kruskal Counts & Linked Lists (Lecture 4):**
    *   *Concept:* Coupling card-counting permutations and word hops into linked-list node chains. Review pointer references in C and indexed target jumping in Fortran.
*   **Past Midterm Archive & Course Codes:**
    *   **`mid-prep-2026.html` and 2025 Midterm Exam Solutions:** Carefully inspect past quiz traps (such as identifying incorrect technical terms inside quadruple asterisks `****word****`).
    *   **`[http://planets.utsc.utoronto.ca/~pawel/progD57](http://planets.utsc.utoronto.ca/~pawel/progD57)`:** Run, inspect, and benchmark the professor’s codes for the 711 puzzle, Kruskal counts, 2D diffusion OpenMP stencils, and Monte Carlo $\pi$ estimation.

---

### Master Reading Checklist Prior to Midterm

```
Pre-Midterm Reading Schedule:
├── Week 1–2 (Linux, Compilers & Languages)
│   ├── Membrey: Ch 3 (CentOS, shells, ssh, /etc/hosts.deny)
│   ├── Schörghofer: Ch 1 (pp. 1–35, language comparison)
│   └── Izaac & Wang: Ch 2 & 3 (Fortran 95 & Python C-bindings)
├── Week 3–4 (A1 Preparation: Dynamics, Stencils, Algorithms)
│   ├── Anderson: Ch 5 (§5.13–§5.16, loop dynamics & stall)
│   ├── Taylor: Ch 2 (§2.1–§2.4, quadratic drag & terminal velocity)
│   ├── CLRS: Ch 3 & 4 (asymptotic proofs for monotonicity scan)
│   ├── Bryant & O'Hallaron: Ch 5 & 6 (cache lines & spatial locality)
│   └── LeVeque: Ch 1 & Newman: Ch 5 (stencil truncation & roundoff envelope)
├── Week 5–6 (A2 Preparation: Monte Carlo & OpenMP)
│   ├── Newman: Ch 10 (random numbers, LCGs, 1/√N error scaling)
│   ├── Hager & Wellein: Ch 6 (OpenMP fork-join, shared/private, reductions)
│   └── LeVeque: Ch 9 (2D diffusion stencils & CFL stability limits)
└── Week 6–7 (Midterm Quiz & Problem Review)
    ├── Hager & Wellein: Ch 1–3 (Dennard scaling, power wall, memory wall)
    ├── King: Ch 11, 12, 17 (C pointers vs. Fortran column-major memory)
    └── Course Archives: mid-prep-2026.html + 2025 Midterm solutions + progD57
```

---

# you asked

message time: 2026-10-03 15:05:56

now jsut give me what to read and in what order to read it

---

# gemini response

### Phase 1: Systems, Shells, and Language Toolchains (Lectures 1–3)

Read these foundational texts first to navigate the cluster environments (`art-1` running CentOS with `tcsh` and `art-16` running Rocky Linux with `bash`), configure remote access, and establish baseline C or Modern Fortran compilation pipelines:

1. **Mark G. Sobell — *A Practical Guide to Linux Commands, Editors, and Shell Programming*** (or **Matthew — *Beginning Linux Programming*, Chapters 1–5**)
   * **Scope to read:** Shell navigation (`cd`, `ls -la`), process control (`ps`, `bg`, `fg`, `kill`, `&`), stream redirection (`>`, `>>`, `|`), and text editors (`vi`/`vim`, `nano`, `micro`).
   * **Shell differences:** Study the syntax variations between `bash` (environment variables via `export VAR=value`, aliases via `alias name='command'`) and `tcsh` (variables via `setenv VAR value`, aliases via `alias name 'command'`).
   * **Explicit exclusions:** Skip sections covering `sed`, `awk`, `perl`, `emacs`, SQL databases, semaphores, pipes/sockets, and low-level POSIX calls.
   * **Networking & security:** Review remote connectivity commands (`ssh`, `sftp`, `traceroute`, `ping`) and securing server access via `/etc/hosts.deny`.

2. **Norbert Schörghofer — *Lessons in Scientific Computing***
   * **Chapter 1 (pp. 25–35):** Read the performance comparisons between compiled languages (C, Fortran 95) and interpreted environments (Python, NumPy, MATLAB, IDL), focusing on why inner loops require compiled binaries.

3. **Language Foundations (Select Your Primary Language: C or Modern Fortran)**
   * **If choosing C:**
     * **Stephen G. Kochan — *Programming in C* (Chapters 7–11)** or **Kernighan & Ritchie (K&R) — *The C Programming Language* (Chapters 1–5):** Focus on arrays, pointer arithmetic, memory addresses, and dynamic allocation via `malloc` and `free`.
     * **K. N. King — *C Programming: A Modern Approach* (Chapters 11, 12, & 17):** Study flattened 1D array indexing (`grid[i * N + j]`) versus jagged pointer arrays (`grid[i][j]`) to understand spatial cache locality.
   * **If choosing Fortran:**
     * **Stephen J. Chapman — *Fortran for Scientists and Engineers* (Chapters 1–8)** (or **Brainerd / Chivers**): Study free-form source formatting, `implicit none`, array operations, modules, and case-insensitivity rules.
     * **Milan Curcic — *Modern Fortran: Building Efficient Parallel Applications* (Chapters 2–5):** Focus on whole-array arithmetic, multidimensional array slices (`A(1:N:2)`), and intrinsic array functions.
   * **For Python Interoperability:**
     * **J. Izaac & J. B. Wang — *Computational Quantum Mechanics* (Chapters 2 & 3):** Read Chapter 2 for Modern Fortran array foundations and Chapter 3 for scientific Python and wrapping compiled C/Fortran routines.

---

### Phase 2: Material for Assignment 1 (Due Lecture 4)

Work through these readings to build the analytical physics formulations, asymptotic algorithmic proofs, and finite-difference stencils required for the four assignment problems:

#### Step 2A: Flight Dynamics and Aerobatic Loop Analysis (Problem 1.1)
* **Robert Resnick, David Halliday, & Kenneth S. Krane (RHK) — *Physics, Vol. 1* (5th Ed.)**
  * **Chapter 4 (§4.5):** Kinematics of relative velocity and constructing airspeed-wind drift vector triangles: $\mathbf{v}_{\text{ground}} = \mathbf{v}_{\text{plane}} + \mathbf{v}_{\text{wind}}$.
  * **Chapters 7 & 8:** Work, kinetic energy, and mechanical energy conservation along vertical arcs: $v(y) = \sqrt{v_0^2 - 2gy}$.
* **John D. Anderson — *Introduction to Flight* (8th/9th Ed.)**
  * **Chapter 5 (§5.13–§5.15):** Normal load factor $n = 1 + v^2/(gR)$, centripetal pull-up force balance, and apex weightlessness determining the circular radius $R = v_0^2/(5g)$.
  * **Chapter 5 (§5.16):** The $V\text{–}n$ flight envelope and dynamic stall speed scaling $v_S(n) = v_{S,0}\sqrt{n}$.
* **John R. Taylor — *Classical Mechanics***
  * **Chapters 1 & 2 (§2.1–§2.4):** Quadratic aerodynamic drag vectors $\mathbf{F}_D = -\frac{1}{2}\rho C_D A v \mathbf{v}$.
  * **Chapter 3 (§3.1–§3.3):** Momentum conservation and center-of-mass decoupling.
* **Bernard Etkin & Lloyd Duff Reid — *Dynamics of Flight: Stability and Control* (3rd Ed.)**
  * **Chapter 5 (§5.1–§5.6):** Coupled longitudinal equations of motion in speed $v(t)$ and flight-path angle $\theta(t)$, and load-dependent induced drag polar modeling: $C_D = C_{D0} + K C_L^2$.
* **William H. Press et al. — *Numerical Recipes* (3rd Ed.) / Mark Newman — *Computational Physics***
  * **Press et al., Chapter 16 (§16.1–§16.3)** or **Newman, Chapter 8 (§8.1–§8.4):** Explicit fourth-order Runge–Kutta (RK4) integration with adaptive step-size control and trajectory closure checks at $\theta = 2\pi$.
* **Vladimir Arnold — *Mathematical Methods of Classical Mechanics* (2nd Ed.)**
  * **Chapter 3 (§12, §16):** Clothoid (Euler spiral) curvature parameterization $\kappa(s) = s/A^2$ to eliminate unbounded normal jerk ($\dot{n} \to \infty$).

#### Step 2B: Multiphase Air-Water Ballistics (Problem 1.2)
* **RHK — *Physics, Vol. 1* (5th Ed.)**
  * **Chapter 15 (§15.1–§15.4):** Fluid statics, hydrostatic pressure variation, Archimedes' buoyancy, and effective gravity in water: $g_{\text{eff}} = g(1 - \rho_w/\rho_p)$.
* **John R. Taylor — *Classical Mechanics***
  * **Chapter 2 (§2.1–§2.4):** Motion in resisting media and closed-form vertical terminal velocity $v_t = \sqrt{2m g_{\text{eff}} / (\rho C_D A)}$.
* **Randall J. LeVeque — *Finite Difference Methods for Ordinary and Partial Differential Equations***
  * **Chapters 1–3:** Initial value problems across discontinuous interfaces and managing severe deceleration spikes across the air-water density boundary.
* **Press et al. — *Numerical Recipes* (3rd Ed.)**
  * **Chapter 9 & Chapter 16 (§16.6):** Brent’s root-finding method for detecting the interface impact zero-crossing $y(t^*)=0$ and managing stiff differential equations.

#### Step 2C: Vector Monotonicity and Memory Optimization (Problem 1.3)
* **Thomas H. Cormen et al. (CLRS) — *Introduction to Algorithms* (3rd/4th Ed.)**
  * **Chapter 3 (§3.1–§3.2) & Chapter 4 (§4.1):** Asymptotic growth notations ($\Theta, \mathcal{O}, \Omega$), algebraic proof that naive pairwise comparisons scale as $\sum_{i=1}^{N-1}(N-i) \in \Theta(N^2)$, and prefix reduction to a linear $\Theta(N)$ scan.
* **Donald E. Knuth — *The Art of Computer Programming, Vol. 2: Seminumerical Algorithms***
  * **Chapters 3 & 4:** Discrete sequence scanning, loop invariants, and proof of single-pass running minimum optimization requiring $\mathcal{O}(1)$ auxiliary storage.
* **Randal E. Bryant & David R. O'Hallaron — *Computer Systems: A Programmer's Perspective (CS:APP)* (3rd Ed.)**
  * **Chapter 5 (§5.7–§5.12):** Program optimization, instruction-level parallelism (ILP), and loop unrolling.
  * **Chapter 6 (§6.2–§6.6):** The memory hierarchy, 64-byte L1/L2/L3 cache lines, spatial locality, and avoiding cache misses during $N \sim 10^7$ element traversals.

#### Step 2D: Second-Derivative Stencil Truncation and Roundoff Limits (Problem 1.4)
* **Randall J. LeVeque — *Finite Difference Methods***
  * **Chapter 1 (§1.1–§1.3):** Taylor series expansions and analytical derivation of the 3-point central difference truncation error bound: $E_{\text{trunc}} = \frac{h^2}{12}|f^{(4)}(\xi)|$.
* **Mark Newman — *Computational Physics***
  * **Chapter 5 (§5.10):** Subtractive floating-point roundoff cancellation: $E_{\text{round}} = \frac{4\epsilon_{\text{mach}}}{h^2}|f|$, derivation of optimal step size $h_{\text{opt}} \sim \epsilon_{\text{mach}}^{1/4}$, and generating the log-log error V-curve.

---

### Phase 3: Material for Assignment 2 (Due Lecture 6)

Read these sources to implement stochastic Monte Carlo simulations and shared-memory parallel programming:

#### Step 3A: Monte Carlo Integration and Error Scaling
* **Mark Newman — *Computational Physics***
  * **Chapter 10 (§10.1):** Pseudo-random number generators, linear congruential generators (LCGs), random seeds, and uniform sampling.
  * **Chapter 10 (§10.2):** Monte Carlo integration methods, including hit-or-miss and mean-value estimation of $\pi$.
  * **Chapter 10 (§10.3):** Statistical errors, the Central Limit Theorem, and proof of the dimension-independent $\sigma \propto \frac{1}{\sqrt{N}}$ convergence rate.
* **Press et al. — *Numerical Recipes* (3rd Ed.)**
  * **Chapter 7 (§7.1–§7.3):** Random number generation, period lengths, and eliminating LCG hyper-plane correlations.
  * **Chapter 15 (§15.1):** Statistical modeling, sample variance, and confidence intervals.

#### Step 3B: OpenMP Loop Parallelization and 2D Diffusion
* **Georg Hager & Gerhard Wellein — *Introduction to High Performance Computing for Scientists and Engineers***
  * **Chapter 6 (§6.1–§6.2):** The fork-join thread execution model and work-sharing loop constructs (`#pragma omp parallel for` in C, `!$omp parallel do` in Fortran).
  * **Chapter 6 (§6.3):** Data scoping rules, thread-safety, distinguishing `shared` arrays from loop-private variables (`private`, `firstprivate`), and preventing data races.
  * **Chapter 6 (§6.4):** Reduction operations (`reduction(+:sum)`) for accumulating multi-threaded Monte Carlo sums across CPU cores.
* **Milan Curcic — *Modern Fortran: Building Efficient Parallel Applications***
  * **Chapters 11 & 12:** Parallelizing loops with OpenMP directives, chunk scheduling (`schedule(static)` vs. `schedule(dynamic)`), and SIMD compiler auto-vectorization.
* **Randall J. LeVeque — *Finite Difference Methods***
  * **Chapter 9:** Parabolic PDEs and explicit 2D 5-point Laplace stencil updates for the diffusion equation:
    $$u_{i,j}^{n+1} = u_{i,j}^n + \Delta t \left( \frac{u_{i+1,j}^n - 2u_{i,j}^n + u_{i-1,j}^n}{\Delta x^2} + \frac{u_{i,j+1}^n - 2u_{i,j}^n + u_{i,j-1}^n}{\Delta y^2} \right)$$
    Managing grid boundary updates in parallel and verifying the numerical CFL stability limit: $\Delta t \le \frac{\Delta x^2}{4D}$.

---

### Phase 4: Midterm Exam Preparation (Lecture 7)

The midterm exam is split into an 8% theoretical quiz and an 8% written problem-solving section (allowing 8 handwritten note pages / 4 double-sided sheets and a calculator). Complete these readings and code inspections in order:

1. **Hardware Architecture, Microprocessors, and Physical Bottlenecks (Quiz Scope)**
   * **Paul E. Ceruzzi — *A History of Modern Computing* (Chapters 5 & 6):** Microprocessor development, Intel x86 architecture, the origins of Unix and Linux, and the growth of the Internet.
   * **Georg Hager & Gerhard Wellein — *Introduction to High Performance Computing*:**
     * **Chapter 1:** Superscalar pipelines, clock frequency ceilings, and SIMD instruction registers.
     * **Chapter 2 (§2.1–§2.3):** Arithmetic intensity (FLOPs per byte of DRAM transfer), cache line latency, and the memory bandwidth wall.
     * **Chapter 3:** The breakdown of Dennard scaling around 2004–2005 due to leakage currents, the processor power wall, the shift to multi-core architectures, and the sustainability of Moore's Law.

2. **Memory Models and Language Standards (Quiz & Problem Scope)**
   * **K. N. King — *C Programming: A Modern Approach* (Chapters 11, 12, 17):** Contrast C row-major (lexicographical) contiguous buffer storage with Fortran column-major storage, and analyze why non-contiguous memory layouts degrade hardware prefetching.
   * **Compiler Toolchains & Flags:** Review GCC (`gcc`, `gfortran`), Intel (`icc`, `ifort`, `ifx`), and NVIDIA (`nvcc`, `nvfortran`) compiler optimization flags (`-O2`, `-O3`, `-fopenmp`, `-march=native`).

3. **Algorithmic Puzzles and Instructor Code Repository (`progD57`)**
   * **The 711 Numerical Puzzle (Lecture 4):** Review the prime factorization of $711 \times 10^6 = 2^6 \cdot 3^2 \cdot 5^6 \cdot 79$ and how constraint pruning (isolating multiples of 79 with ordered loops $a \le b \le c \le d$) eliminates brute-force $\mathcal{O}(N^4)$ search costs.
   * **Kruskal Counts & Linked Lists (Lecture 4):** Trace how deterministic hopping over card sequences maps directly to linked-list node chains in C pointers and Fortran array indices.
   * **Live Code Inspection:** Download, compile, and run the professor's sample codes at `[http://planets.utsc.utoronto.ca/~pawel/progD57](http://planets.utsc.utoronto.ca/~pawel/progD57)` for the 711 puzzle, Kruskal counts, OpenMP Monte Carlo $\pi$ calculations, and the parallel 2D diffusion stencil.
   * **Exam Archives:** Review `mid-prep-2026.html` and the 2025 Midterm Exam solutions, paying close attention to quiz traps where incorrect technical terms are enclosed in quadruple asterisks (`****word****`).