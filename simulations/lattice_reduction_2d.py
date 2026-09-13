#!/usr/bin/env python3
"""
Gauss-Lagrange 2D Lattice Basis Reduction Simulator.
Computes the shortest basis vectors and minimal Wigner-Seitz unit cell for crystallographic lattices.
"""

import math
from typing import Tuple

Vector2D = Tuple[float, float]

def dot(u: Vector2D, v: Vector2D) -> float:
    return u[0] * v[0] + u[1] * v[1]

def norm_sq(u: Vector2D) -> float:
    return dot(u, u)

def norm(u: Vector2D) -> float:
    return math.sqrt(norm_sq(u))

def gauss_reduction(v1: Vector2D, v2: Vector2D) -> Tuple[Vector2D, Vector2D, int]:
    """
    Applies the Gauss-Lagrange 2D lattice reduction algorithm.
    Returns (u, v, step_count) where ||u|| <= ||v|| and |dot(u, v)| / ||u||^2 <= 0.5.
    """
    u, v = v1, v2
    steps = 0

    while True:
        steps += 1
        # 1. Ensure ||u|| <= ||v||
        if norm_sq(u) > norm_sq(v):
            u, v = v, u

        # 2. Compute projection scalar mu = (u . v) / ||u||^2
        mu = dot(u, v) / norm_sq(u)
        q = round(mu)

        if q == 0:
            break

        # 3. Reduce v by integer multiple of u
        v = (v[0] - q * u[0], v[1] - q * u[1])

        # 4. If v became strictly shorter than u, swap and repeat
        if norm_sq(v) < norm_sq(u):
            u, v = v, u

    return u, v, steps

if __name__ == "__main__":
    # Highly skewed, non-orthogonal crystallographic lattice basis
    b1 = (101.0, 312.0)
    b2 = (205.0, 627.0)

    print("=== PHYD57 2D Gauss-Lagrange Crystallography Lattice Reduction ===")
    print(f"Initial Basis Vectors:")
    print(f"  v1 = {b1}, ||v1|| = {norm(b1):.4f}")
    print(f"  v2 = {b2}, ||v2|| = {norm(b2):.4f}")

    u, v, steps = gauss_reduction(b1, b2)

    print(f"\nReduced Optimal Wigner-Seitz Basis (converged in {steps} steps):")
    print(f"  u  = {u}, ||u||  = {norm(u):.4f}")
    print(f"  v  = {v}, ||v||  = {norm(v):.4f}")
    orthogonality_defect = abs(dot(u, v)) / (norm(u) * norm(v))
    print(f"  Cosine of angle (orthogonality defect): {orthogonality_defect:.6f}")
