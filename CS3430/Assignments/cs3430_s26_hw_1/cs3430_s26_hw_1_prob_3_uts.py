#############################################################
# cs3430_s26_hw_1_prob_3_uts.py
# unit tests for CS3430 S26 HW1 Prob 3
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

from cs3430_s26_hw_1_prob_3 import naive_sum, sorted_sum, kahan_sum

"""
I used math.fsum in the unit tests below. It computes a floating-point 
sum using a carefully designed algorithm that tracks partial sums 
internally to reduce rounding error. It is much more accurate than naive 
summation and is specifically intended for numerical work.

In this assignment, math.fsum is used as a high-accuracy reference,
not because it is exact, but because it significantly reduces error
compared to simple summation methods.

Our goal is not to reimplement math.fsum, but to understand why
naive summation fails and how algorithms like Kahan summation 
improve numerical stability.
"""

class TestSummationMethods(unittest.TestCase):
    """
    Unit tests for Problem 3: Floating-Point Summation.

    These tests compare three summation strategies:
      - naive summation (order-sensitive),
      - summation after sorting by magnitude,
      - Kahan compensated summation.

    We use math.fsum as a high-accuracy reference.
    """

    def test_basic_correctness_small(self):
        print("\n[Test] Basic correctness on small input")

        xs = [0.1, 0.2, 0.3, -0.6, 1.0]
        ref = math.fsum(xs)

        v_naive = naive_sum(xs)
        v_sorted = sorted_sum(xs)
        v_kahan = kahan_sum(xs)

        print(f"Input values: {xs}")
        print(f"math.fsum   = {ref:.16e}")
        print(f"naive_sum   = {v_naive:.16e}")
        print(f"sorted_sum  = {v_sorted:.16e}")
        print(f"kahan_sum   = {v_kahan:.16e}")

        self.assertAlmostEqual(v_naive, ref, places=15)
        self.assertAlmostEqual(v_sorted, ref, places=15)
        self.assertAlmostEqual(v_kahan, ref, places=15)

    def test_order_sensitivity_large_small_mix(self):
        print("\n[Test] Order sensitivity with large/small mixture")

        big = 1e16
        tiny = 1.0
        N = 1_000_000

        xs_bad = [big] + [tiny] * N + [-big]
        xs_good = [big, -big] + [tiny] * N

        ref_bad = math.fsum(xs_bad)
        ref_good = math.fsum(xs_good)

        print(f"Expected sum (reference) = {ref_bad:.1f}")

        v_naive_bad = naive_sum(xs_bad)
        v_sorted_bad = sorted_sum(xs_bad)
        v_kahan_bad = kahan_sum(xs_bad)

        print("Bad order results:")
        print(f"naive_sum   = {v_naive_bad:.16e}")
        print(f"sorted_sum  = {v_sorted_bad:.16e}")
        print(f"kahan_sum   = {v_kahan_bad:.16e}")

        self.assertEqual(ref_bad, float(N))
        self.assertLessEqual(abs(v_sorted_bad - ref_bad),
                             abs(v_naive_bad - ref_bad))
        self.assertLessEqual(abs(v_kahan_bad - ref_bad),
                             abs(v_naive_bad - ref_bad))

        v_naive_good = naive_sum(xs_good)
        print("Good order naive result:")
        print(f"naive_sum   = {v_naive_good:.16e}")

        self.assertAlmostEqual(v_naive_good, ref_good, places=9)

    def test_kahan_improves_over_naive_on_bad_order(self):
        print("\n[Test] Kahan summation improves over naive summation")

        big = 1e16
        N = 1_000_000
        xs = [big] + [1.0] * N + [-big]

        ref = math.fsum(xs)
        v_naive = naive_sum(xs)
        v_kahan = kahan_sum(xs)

        err_naive = abs(v_naive - ref)
        err_kahan = abs(v_kahan - ref)

        print(f"Reference sum = {ref:.1f}")
        print(f"naive_sum    = {v_naive:.16e}")
        print(f"kahan_sum    = {v_kahan:.16e}")
        print(f"err_naive    = {err_naive:.3e}")
        print(f"err_kahan    = {err_kahan:.3e}")

        self.assertLessEqual(err_kahan, err_naive)

    def test_sorted_sum_helps_on_constructed_case(self):
        print("\n[Test] Sorted summation on constructed example")

        xs = [1e20, 1.0, 1.0, 1.0, -1e20]  # true sum = 3.0
        ref = math.fsum(xs)

        v_naive = naive_sum(xs)
        v_sorted = sorted_sum(xs)

        print(f"Input values: {xs}")
        print(f"math.fsum   = {ref:.1f}")
        print(f"naive_sum   = {v_naive:.16e}")
        print(f"sorted_sum  = {v_sorted:.16e}")

        self.assertEqual(ref, 3.0)
        self.assertLessEqual(abs(v_sorted - ref),
                             abs(v_naive - ref))


if __name__ == "__main__":
    print("\nRunning CS3430 S26 HW1 Problem 3 unit tests...\n")
    unittest.main()
    pass
    
### Your interpretation comments here inside """ """.

"""
CS3430 HW1 Problem 3 Interpretations:

Unit Test 1: Basic correctess on small input

Results:

    [Test] Basic correctness on small input
    Input values: [0.1, 0.2, 0.3, -0.6, 1.0]
    math.fsum   = 1.0000000000000000e+00
    naive_sum   = 1.0000000000000000e+00
    sorted_sum  = 1.0000000000000000e+00
    kahan_sum   = 1.0000000000000000e+00

My Interpretation:

    The builtin python sum function, the naive_sum, the sorted_sum, and the
    kahan_sum all give the same result for this input set. 

    The numbers in the input set are modest and not insanely small or large,
    so errors due to floating point precision are minor.

Unit Test 2: Kahan Summation Improves Over Naive Summation

    [Test] Kahan summation improves over naive summation
    .Reference sum = 1000000.0
    naive_sum    = 0.0000000000000000e+00
    kahan_sum    = 1.0000000000000000e+06
    err_naive    = 1.000e+06
    err_kahan    = 0.000e+00

My Interpretation:

    In this unit test, the niave sum fails. It gives a result of 0, which is way off from 1,000,000
    The Kahan summation method gives the correct result of 1,000,000 with no error.

    The reason for this is because the naive summation is sensitive to the order of the inputs.

    The naive summation is sensitive to the order of the inputs because, if it starts off with a large number, 
    due to floating point rounding, the small numbers that follow the large number will get lost and be negligible
    when added to the large number.

    In this example 1e16 is added first, and then 1.0 is added a million times, and then -1e16 is added last. But, by the time
    we get to -1e16, all the 1.0 additions have been lost due to floating point rounding, so the final answer is is basically 1e16 - 1e16
    which is just 0.


Unit Test 3: Order Sensitivity with large/small mixture

Results:

    [Test] Order sensitivity with large/small mixture
    .Expected sum (reference) = 1000000.0
    Bad order results:
    naive_sum   = 0.0000000000000000e+00
    sorted_sum  = 1.0000000000000000e+06
    kahan_sum   = 1.0000000000000000e+06
    Good order naive result:
    naive_sum   = 1.0000000000000000e+06

My Interpretation:

    Like unit test 2, this unit test also shows how the naive summation is sensitive to the order of the inputs.
    In the bad order, the naive summation gives a result of 0, which is way off from the expected result of 1,000,000.

    However, in a good order the niave sum works as it should and gives the answer of 1,000,000. 

    Sorting by magnitude improves accuracy because we then add the small numbers first. Adding the small number first reduces the
    chance for rounding errors to occur compared to when adding the large numbers first like in unit test 2.

    Kahan summation reduces numerical error by storing the accumulated rounding error in a seperate variable, c, and then
    adds that error back in. This way, you can add in any order and all the small numbers won't get lost. 

    These results demonstrate that floating point addition is not associative, because the order of addition can drastically change the
    final answer because of rounding errors. Floating point math is not the same as real number math, because we are working with a confined space
    infinity does not exist here.

Unit Test 4: Sorted Summation on constructed example

Results:

    [Test] Sorted summation on constructed example
    Input values: [1e+20, 1.0, 1.0, 1.0, -1e+20]
    math.fsum   = 3.0
    naive_sum   = 0.0000000000000000e+00
    sorted_sum  = 0.0000000000000000e+00

My Interpretation:

    In this test both the naive and sorted are wrong. This is sorted_sums first time being wrong in these unit tests.

    The reason sorted_sum fails here is because the small numbers are still being added to a large number.
    Even though the magnitutes are sorted, the large numbers are still overshadowing the small numbers, and makes
    their addition negligible due to floating point rounding.

    This means that even sorting is not a good enough solution.

"""