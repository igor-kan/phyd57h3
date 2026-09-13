#!/usr/bin/env python3
"""
PHYD57 Unit Test Suite: Numerical Number Theory & Lattice Primitives.
"""

import math
from lattice_reduction_2d import gauss_reduction, norm_sq, dot

def test_gauss_reduction():
    # Test on standard orthogonal lattice
    u, v, _ = gauss_reduction((1.0, 0.0), (0.0, 1.0))
    assert math.isclose(norm_sq(u), 1.0)
    assert math.isclose(norm_sq(v), 1.0)
    assert math.isclose(dot(u, v), 0.0)

    # Test on skewed lattice
    u, v, steps = gauss_reduction((10.0, 0.0), (10.0, 1.0))
    assert norm_sq(u) <= norm_sq(v)
    assert abs(dot(u, v)) / norm_sq(u) <= 0.5 + 1e-9
    print(f"✓ Gauss reduction verified across orthogonal and skewed test cases ({steps} steps).")

if __name__ == "__main__":
    test_gauss_reduction()
    print("🎉 All PHYD57 number theory tests passed!")
