#############################################################
# cs3430_s26_hw_1_prob_2_uts.py
# unit tests for CS3430 S26 HW1 Prob 2
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
import math

from cs3430_s26_hw_1_prob_2 import g_naive, g_stable, g_ref, compare_errors


class TestCancellationAndStability(unittest.TestCase):
    """
    Unit tests for Problem 2: Cancellation and Numerical Stability.

    These tests compare:
      - a naive formula,
      - a numerically stable reformulation,
      - and a Taylor-series reference approximation.

    The printed output is intended to help students
    observe cancellation and stability directly.
    """

    def test_ref_is_reasonable_near_zero(self):
        print("\n[Test] Reference approximation near zero")
        for x in [1e-4, 1e-6, 1e-8]:
            r = g_ref(x)
            expected = 0.5 - (x*x)/24.0 + (x*x*x*x)/720.0
            print(f"x = {x: .1e}  g_ref(x) = {r:.16e}")
            self.assertAlmostEqual(r, expected, places=15)

    def test_naive_and_stable_agree_for_moderate_x(self):
        x = 1e-1
        v_naive = g_naive(x)
        v_stable = g_stable(x)

        print("\n[Test] Naive vs Stable for moderate x")
        print(f"x = {x}")
        print(f"g_naive(x)  = {v_naive:.16e}")
        print(f"g_stable(x) = {v_stable:.16e}")
        print(f"abs diff    = {abs(v_naive - v_stable):.3e}")

        self.assertAlmostEqual(v_naive, v_stable, places=12)

    def test_stable_is_better_for_tiny_x(self):
        x = 1e-8
        r = g_ref(x)
        v_naive = g_naive(x)
        v_stable = g_stable(x)

        err_naive = abs(v_naive - r)
        err_stable = abs(v_stable - r)

        print("\n[Test] Cancellation for tiny x")
        print(f"x = {x}")
        print(f"g_ref(x)    = {r:.16e}")
        print(f"g_naive(x)  = {v_naive:.16e}")
        print(f"g_stable(x) = {v_stable:.16e}")
        print(f"err_naive   = {err_naive:.3e}")
        print(f"err_stable  = {err_stable:.3e}")

        self.assertLess(err_stable, err_naive)

    def test_compare_errors_shape(self):
        xs = [1e-1, 1e-3, 1e-5, 1e-7, 1e-8]
        rows = compare_errors(xs)

        print("\n[Test] Error comparison table")
        print("x        | err_naive        | err_stable")
        print("------------------------------------------")
        for (x, errn, errs) in rows:
            print(f"{x: .1e} | {errn: .3e} | {errs: .3e}")
            self.assertGreaterEqual(errn, 0.0)
            self.assertGreaterEqual(errs, 0.0)

        self.assertEqual(len(rows), len(xs))

    def test_stable_tracks_reference_well(self):
        print("\n[Test] Stable formula tracks reference")
        for x in [1e-6, 1e-8]:
            v_stable = g_stable(x)
            r = g_ref(x)
            diff = abs(v_stable - r)

            print(f"x = {x: .1e}")
            print(f"g_stable(x) = {v_stable:.16e}")
            print(f"g_ref(x)    = {r:.16e}")
            print(f"abs diff    = {diff:.3e}")

            self.assertAlmostEqual(v_stable, r, places=12)


if __name__ == "__main__":
    print("\nRunning CS3430 S26 HW1 Problem 2 unit tests...\n")
    unittest.main()
    pass
    
### Your interpretation comments here inside """ """.

"""
CS3430 HW1 Problem 2 Interpretations:

Unit Test 1: Error Comparison Table

Results:

    [Test] Error comparison table
    x        | err_naive        | err_stable
    ------------------------------------------
    1.0e-01 |  2.480e-11 |  2.480e-11
    1.0e-03 |  7.831e-12 |  0.000e+00
    1.0e-05 |  4.137e-08 |  5.551e-17
    1.0e-07 |  3.996e-04 |  5.551e-17
    1.0e-08 |  5.000e-01 |  0.000e+00

My Interpretation:

    As X gets smaller The naive errors get significantly larger while the stable errors remain 
    very small, even reaching 0. 
    
    When X is 1.0e-08 the naive error is 0.5 which is HUGE compared to The stable error of 0. 
    This shows that g_naive(x) is innacurate for very small x values due to Loss of significance

    naive and stable agree for moderate values of X because catastrophic cancellation is not an issue for the larger
    values of X, but as X goes closer to 0 the naive formula starts subtracting nearly equal numbers
    Which causes the error to grow. 
 
Unit Test 2: Naive Vs Stable for Moderate x

Results:

    [Test] Naive vs Stable for moderate x
    x = 0.1
    g_naive(x)  = 4.9958347219741783e-01
    g_stable(x) = 4.9958347219742333e-01
    abs diff    = 5.496e-15

My Interpretation:

    When X is moderate, for example 0.1, Both the naive and stable formulas give very similar results
    with a very small absolute difference of 5.496e-15.

    This is because the cancellation is not a big issue for moderate values of X, which we also saw
    In the error comparison table in unit test #1.


Unit Test 3: Reference Approximation Near Zero

Results:

    [Test] Reference approximation near zero
    x =  1.0e-04  g_ref(x) = 4.9999999958333335e-01
    x =  1.0e-06  g_ref(x) = 4.9999999999995831e-01
    x =  1.0e-08  g_ref(x) = 5.0000000000000000e-01

My Interpretation:

    As X approaches 0 g_ref(x) approaches 0.5, which matches the limit of g(x) as x approaches 0.
    
    
Unit Test 4: Cancellation for Tiny x

Results:

    [Test] Cancellation for tiny x
    x = 1e-08
    g_ref(x)    = 5.0000000000000000e-01
    g_naive(x)  = 0.0000000000000000e+00
    g_stable(x) = 5.0000000000000000e-01
    err_naive   = 5.000e-01
    err_stable  = 0.000e+00

My Interpretation:

    When X is very small, like 1e-08, g_naive(x) gives us a result of 0.0 which is way off
    from the g_ref(x) value of 0.5. 

    This is because of catastrophic cancellation in the naive formula.

    The G_stable(x) formula avoids cancellation and matches the g_ref(x) value exactly. 

Unit Test 5: Stable Formula Tracks Reference

Results:

    [Test] Stable formula tracks reference
    x =  1.0e-06
    g_stable(x) = 4.9999999999995831e-01
    g_ref(x)    = 4.9999999999995831e-01
    abs diff    = 0.000e+00
    x =  1.0e-08.....


    g_stable(x) = 5.0000000000000000e-01
    g_ref(x)    = 5.0000000000000000e-01
    abs diff    = 0.000e+00


My Interpretation:

    Similar to the other test, this shows that the stable formula matches the reference formula very closely. 
    The stable formula avoids cancellation issues and is much more accurate for small x values/

    G_stable(x) tracks the rerference approximation better than g_naive(x) because it avoids subtracting nearly equal numbers which
    means there are no cancellation errors.

    This behavior illustrates the difference between mathematical correctness and numerical stability by showing that even though
    the niave formula is mathemtaically correct, its not stable in floating point math because of loss of significance errors. 

"""