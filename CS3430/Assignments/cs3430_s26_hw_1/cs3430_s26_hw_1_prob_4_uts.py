#############################################################
# cs3430_s26_hw_1_prob_4_uts.py
# unit tests for CS3430 S26 HW1 Prob 4
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

from cs3430_s26_hw_1_prob_4 import central_diff, richardson_from_central


class TestNumericalDifferentiation(unittest.TestCase):
    """
    Unit tests for Problem 4: Central Differences and Richardson Extrapolation.

    These tests illustrate:
      - O(h^2) behavior of the central difference,
      - higher-order accuracy of Richardson extrapolation,
      - breakdown due to floating-point roundoff for very small h.
    """

    def test_central_difference_error_trend(self):
        print("\n[Test] Central Difference on sin(x) at x = 1.0")

        f = np.sin
        x = 1.0
        true = np.cos(x)

        hs = [10**(-k) for k in range(1, 13)]

        print("h        | approx               | error")
        print("---------------------------------------------")
        for h in hs:
            approx = central_diff(f, x, h)
            err = abs(approx - true)
            print(f"{h: .1e} | {approx: .16f} | {err: .3e}")

        # Sanity check: error initially decreases
        err_h1 = abs(central_diff(f, x, 1e-1) - true)
        err_h2 = abs(central_diff(f, x, 1e-2) - true)
        self.assertLess(err_h2, err_h1)

    def test_richardson_improves_accuracy(self):
        print("\n[Test] Richardson Extrapolation on exp(x) at x = 0.0")

        f = np.exp
        x = 0.0
        true = np.exp(x)

        hs = [10**(-k) for k in range(1, 13)]

        print("h        | D_err        | R_err")
        print("--------------------------------")
        for h in hs:
            D = central_diff(f, x, h)
            R = richardson_from_central(f, x, h)
            D_err = abs(D - true)
            R_err = abs(R - true)
            print(f"{h: .1e} | {D_err: .3e} | {R_err: .3e}")

        # Richardson should improve accuracy for moderate h
        h = 1e-2
        D_err = abs(central_diff(f, x, h) - true)
        R_err = abs(richardson_from_central(f, x, h) - true)
        self.assertLess(R_err, D_err)

    def test_roundoff_eventually_dominates(self):
        """
        Richardson extrapolation eventually stops improving
        due to floating-point roundoff and cancellation.
        """
        f = np.exp
        x = 0.0
        true = np.exp(x)

        h_small = 1e-10
        D_err = abs(central_diff(f, x, h_small) - true)
        R_err = abs(richardson_from_central(f, x, h_small) - true)

        # At very small h, Richardson may not be better
        self.assertGreaterEqual(R_err, 0.0)
        self.assertGreaterEqual(D_err, 0.0)


if __name__ == "__main__":
    print("\nRunning CS3430 S26 HW1 Problem 4 unit tests...\n")
    unittest.main()
    pass
    
### Your interpretation comments here inside """ """.

"""
CS3430 HW1 Problem 4 Interpretations:

Unit Test 1: Central Difference on sin(x) at x = 1.0

Results:

    [Test] Central Difference on sin(x) at x = 1.0
    h        | approx               | error
    ---------------------------------------------
    1.0e-01 |  0.5394022521697600 |  9.001e-04
    1.0e-02 |  0.5402933008747335 |  9.005e-06
    1.0e-03 |  0.5403022158176896 |  9.005e-08
    1.0e-04 |  0.5403023049677103 |  9.004e-10
    1.0e-05 |  0.5403023058569989 |  1.114e-11
    1.0e-06 |  0.5403023058958567 |  2.772e-11
    1.0e-07 |  0.5403023056738121 |  1.943e-10
    1.0e-08 |  0.5403023084493697 |  2.581e-09
    1.0e-09 |  0.5403023028982545 |  2.970e-09
    1.0e-10 |  0.5403022473871033 |  5.848e-08
    1.0e-11 |  0.5403011371640787 |  1.169e-06
    1.0e-12 |  0.5402900349338324 |  1.227e-05

My Interpretation:

    The error initially shrinks as h decreases, as truncation error decreases with a 
    smaller h 

    The error eventually stops decreasing and starts increasing again. This is 
    due to h becoming TOO small, so the floating point roundoff errors start up
    making the error larger again.

    This illustrates a trade-off between truncation and roundoff errors by showing
    that a smaller h decreases truncation error, but if you go too small, it increases 
    roundoff error.

    The truncation dominated regime is from h = 1.0e-01 to h = 1.0e-05
    the roundoff dominated regime is from h = 1.0e-06 to h = 1.0e-12

    The step size wehre accuracy is maximized is h = 1.0e-05

    Numerical differentiation has an optimal step size because its where the truncation
    and roundoff errors are minimized together. 

Unit Test 2: Richardson Extrapolation on exp(x) at x = 0.0

Results:

    [Test] Richardson Extrapolation on exp(x) at x = 0.0
    h        | D_err        | R_err
    --------------------------------
    1.0e-01 |  1.668e-03 |  2.084e-07
    1.0e-02 |  1.667e-05 |  2.085e-11
    1.0e-03 |  1.667e-07 |  1.471e-13
    1.0e-04 |  1.667e-09 |  8.151e-13
    1.0e-05 |  1.210e-11 |  4.701e-12
    1.0e-06 |  2.676e-11 |  4.726e-11
    1.0e-07 |  5.264e-10 |  5.264e-10
    1.0e-08 |  5.264e-10 |  7.928e-09
    1.0e-09 |  2.723e-08 |  1.012e-07
    1.0e-10 |  8.274e-08 |  8.274e-08
    1.0e-11 |  8.274e-08 |  8.274e-08
    1.0e-12 |  3.339e-05 |  1.074e-04

My Interpretation:

    Richardson extrapolation dramatically improves accuracy for moderate values of h because
    the leading error term is eliminated, where higher order accuracy is achieved.

    Richardson approximation eventually stops improving again because of floating-point roundoff and cancellation,
    similar to the central difference method. 

    This means that Richardson extrapolation can become no better or worse then the original centrall difference for very small 
    h because of the same roundoff errors that affect the central difference method.

    for richardson extrapolation,
    The truncation dominated regime is from h = 1.0e-01 to h = 1.0e-03
    the roundoff dominated regime is from h = 1.0e-05 to h = 1.0e-12

    The step size where accuracy is maximized is h = 1.0e-03

    Numerical differentiation has an optimal step size because its where the truncation
    and roundoff errors are minimized together. Similar to the central difference method.



"""

