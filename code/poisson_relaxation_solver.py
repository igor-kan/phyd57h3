"""
PHYD57: 2D Poisson Equation Solver via Successive Over-Relaxation (SOR)
Computes electrostatic potential and electric field vector streamlines on a 2D grid.
"""

import numpy as np
import matplotlib.pyplot as plt

def solve_poisson_sor(N=64, max_iter=5000, tol=1e-5):
    h = 1.0 / (N - 1)
    phi = np.zeros((N, N))
    rho = np.zeros((N, N))

    # Boundary conditions: grounded outer walls (phi = 0)
    # Interior charged plates: +100V and -100V
    plate_width = N // 4
    plate_y1 = N // 3
    plate_y2 = 2 * N // 3
    x_start = N // 3
    x_end = x_start + plate_width

    # Fixed potential mask
    fixed_mask = np.zeros((N, N), dtype=bool)
    fixed_mask[0, :] = fixed_mask[-1, :] = fixed_mask[:, 0] = fixed_mask[:, -1] = True
    
    # Positive plate
    phi[plate_y1, x_start:x_end] = 100.0
    fixed_mask[plate_y1, x_start:x_end] = True
    
    # Negative plate
    phi[plate_y2, x_start:x_end] = -100.0
    fixed_mask[plate_y2, x_start:x_end] = True

    # Optimal SOR parameter for square grid
    omega = 2.0 / (1.0 + np.pi / N)

    for it in range(max_iter):
        phi_old = phi.copy()
        
        # Red-Black or standard Gauss-Seidel with SOR
        for i in range(1, N - 1):
            for j in range(1, N - 1):
                if not fixed_mask[i, j]:
                    phi_gs = 0.25 * (phi[i+1, j] + phi[i-1, j] + phi[i, j+1] + phi[i, j-1])
                    phi[i, j] = (1.0 - omega) * phi[i, j] + omega * phi_gs

        max_diff = np.max(np.abs(phi - phi_old))
        if max_diff < tol:
            print(f"SOR converged in {it} iterations (tol = {tol}, omega = {omega:.3f})")
            break

    # Calculate Electric Field: E = -grad(phi)
    Ey, Ex = np.gradient(-phi, h)
    return phi, Ex, Ey

if __name__ == '__main__':
    N = 64
    phi, Ex, Ey = solve_poisson_sor(N=N)
    
    plt.figure(figsize=(8, 7))
    cp = plt.contourf(phi, levels=30, cmap='RdBu_r', origin='lower')
    plt.colorbar(cp, label=r'Potential $\phi(x,y)$ [V]')
    
    # Streamplot of Electric Field
    x = np.arange(N)
    y = np.arange(N)
    plt.streamplot(x, y, Ex, Ey, color='black', linewidth=0.8, density=1.2, arrowsize=0.8)
    
    plt.title('PHYD57: 2D Electrostatic Potential & Field Lines (SOR Solver)', fontsize=12, fontweight='bold')
    plt.xlabel('Grid Index $x$')
    plt.ylabel('Grid Index $y$')
    plt.tight_layout()
    plt.savefig('poisson_sor_solution.png', dpi=200)
    print("Saved poisson_sor_solution.png")
