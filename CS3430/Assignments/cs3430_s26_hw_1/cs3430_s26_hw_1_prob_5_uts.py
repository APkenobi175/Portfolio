#############################################################
# cs3430_s26_hw_1_prob_5_uts.py
# unit tests for CS3430 S26 HW1 Prob 5
# bugs to vladimir kulyukin in canvas
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
#############################################################

import unittest
import numpy as np
import sympy as sp

from cs3430_s26_hw_1_prob_5 import trap, romberg


class TestRombergIntegration(unittest.TestCase):
    """
    Unit tests for Problem 5: Trapezoidal Rule and Romberg Integration.

    These tests demonstrate:
      - slow convergence of the trapezoidal rule,
      - rapid convergence of Romberg integration,
      - comparison with symbolic (SymPy) reference results.
    """

    def test_symbolic_reference(self):
        print("\n[Test] Symbolic reference using SymPy")

        x = sp.Symbol('x')
        f_sym = sp.sin(x) * sp.exp(x)
        df_sym = sp.diff(f_sym, x)

        print("Symbolic derivative df_sym =", df_sym)

        f = sp.lambdify(x, f_sym, "numpy")
        df = sp.lambdify(x, df_sym, "numpy")

        x0 = 1.0
        true = df(x0)

        print("Reference derivative at x = 1.0 =", true)

        self.assertTrue(np.isfinite(true))

    def test_romberg_on_pi(self):
        print("\n[Test] Romberg integration for pi")

        f = lambda x: 4.0 / (1.0 + x ** 2)

        a, b = 0.0, 1.0
        K = 6

        R = romberg(f, a, b, K)

        print("Romberg table:")
        print(R)

        best = R[K, K]
        err = abs(best - np.pi)

        print("Best estimate:", best)
        print("Error vs pi:", err)

        self.assertLess(err, 1e-12)

    def test_trapezoid_vs_romberg(self):
        print("\n[Test] Trapezoidal rule vs Romberg convergence")

        f = lambda x: 4.0 / (1.0 + x ** 2)
        a, b = 0.0, 1.0

        n = 2 ** 6
        trap_val = trap(f, a, b, n)

        R = romberg(f, a, b, K=6)
        romberg_val = R[6, 6]

        print("Trapezoid estimate:", trap_val)
        print("Romberg estimate:", romberg_val)
        print("True value (pi):", np.pi)

        err_trap = abs(trap_val - np.pi)
        err_rom = abs(romberg_val - np.pi)

        print("Trap error:", err_trap)
        print("Romberg error:", err_rom)

        self.assertLess(err_rom, err_trap)


if __name__ == "__main__":
    print("\nRunning CS3430 S26 HW1 Problem 5 unit tests...\n")
    unittest.main()
    pass
    
### Your interpretation comments here inside """ """.

"""
CS3430 HW1 Problem 5 Interpretations:

Unit Test 1: Romberg integration for pi

Results:

    [Test] Romberg integration for pi
    Romberg table:
    [[3.         0.         0.         0.         0.         0.
    0.        ]
    [3.1        3.13333333 0.         0.         0.         0.
    0.        ]
    [3.13117647 3.14156863 3.14211765 0.         0.         0.
    0.        ]
    [3.13898849 3.1415925  3.14159409 3.14158578 0.         0.
    0.        ]
    [3.14094161 3.14159265 3.14159266 3.14159264 3.14159267 0.
    0.        ]
    [3.14142989 3.14159265 3.14159265 3.14159265 3.14159265 3.14159265
    0.        ]
    [3.14155196 3.14159265 3.14159265 3.14159265 3.14159265 3.14159265
    3.14159265]]
    Best estimate: 3.1415926535897216
    Error vs pi: 7.149836278586008e-14

My Interpretation:

    The first column of the table shows the trapezoidal rule. 
    Each next column shows the romberg extrapolation, which you 
    can see improves the accuracy.
    
    Trapazeoidal rule converges slowly to pi because it 
    approximates the area under the curve using straight lines,
    which is not very accurate for curves like 4/(1+x^2).

    The trapezoidal rule has truncation error on O(h^2), which means 
    you need to reduce h a lot to get good accuracy.

    Romberg integration accelerates convergance because it 
    uses Richardson extrapolation to combine trapezoidal estimates,
    which in turn cancels out leading error terms.

    Richardson extrapololation improves accuracy by using multiple estimates
    with different step sizes.



Unit Test 2: Symbolic reference using SymPy

Results:

    [Test] Symbolic reference using SymPy
    Symbolic derivative df_sym = exp(x)*sin(x) + exp(x)*cos(x)
    Reference derivative at x = 1.0 = 3.7560492270947274

My Interpretation:
    
    Symbolic computation differs from numerical approximation because
    symbolic computation provides an exact expression, where numerical
    provides an approximate discrete value.

    The symbolic derivative is solved similar to how we would
    have done it by hand in a calculus class, using the product rule.

    Then, the expression is evaluated at x = 1.0 to get the ref value.
    Which, we would lambdify to use in numerical tests.

Unit Test 3: Trapezoidal rule vs Romberg convergence

Results:

    [Test] Trapezoidal rule vs Romberg convergence
    ..Trapezoid estimate: 3.141551963485655
    Romberg estimate: 3.1415926535897216
    True value (pi): 3.141592653589793
    Trap error: 4.069010413809693e-05
    Romberg error: 7.149836278586008e-14

My Interpretation:

    This unit test shows off the slow convergance of the trapezoidal rule
    compared to the rapid convergance of Romberg integration.

    This also shows that the romberg integration is much more accurate
    than the trapezoidal rule for the same number of subintervals.

    Romberg can achieve near machine precision accuracy because it uses
    richardson extrapolation to basically cancel out leading error terms. 
    It also combines multiple trapezoidal estimates to get a more accurate result.

 
"""