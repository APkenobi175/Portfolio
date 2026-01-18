#############################################################
# cs3430_s26_hw_1_prob_1_uts.py
# unit tests for CS3430 S26 HW1 Prob 1
# bugs to vladimir kulyukin in canvas
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
##############################################################

import math
import unittest

from cs3430_s26_hw_1_prob_1 import float_gap, machine_epsilon


class TestFloatingPointGaps(unittest.TestCase):
    """
    Unit tests for Problem 1: Floating-point gaps and machine epsilon.

    These tests verify both numerical correctness and
    conceptual properties discussed in Lecture 1:
      - uneven spacing of floating-point numbers,
      - definition and behavior of machine epsilon,
      - relationship between epsilon and spacing near 1.0.
    """

    def test_gap_near_one(self):
        print("\n[Test] Gap near 1.0")

        gap_1 = float_gap(1.0)
        ref_gap_1 = math.nextafter(1.0, math.inf) - 1.0

        print(f"Computed gap at 1.0      = {gap_1:.18e}")
        print(f"Reference gap (nextafter)= {ref_gap_1:.18e}")

        rel_err = abs(gap_1 - ref_gap_1) / ref_gap_1
        print(f"Relative error           = {rel_err:.3e}")

        self.assertLess(rel_err, 1e-12)

    def test_gap_near_large_number(self):
        print("\n[Test] Gap near 1e10 vs gap near 1.0")

        gap_1 = float_gap(1.0)
        gap_1e10 = float_gap(1e10)

        print(f"Gap near 1.0  = {gap_1:.18e}")
        print(f"Gap near 1e10 = {gap_1e10:.18e}")
        print(f"Ratio (1e10 / 1.0) = {gap_1e10 / gap_1:.3e}")

        self.assertGreater(gap_1e10, gap_1 * 1e6)

    def test_machine_epsilon_properties(self):
        print("\n[Test] Machine epsilon properties")

        eps = machine_epsilon()

        print(f"Computed machine epsilon = {eps:.18e}")
        print(f"1.0 + eps     = {1.0 + eps:.18e}")
        print(f"1.0 + eps/2.0 = {1.0 + eps/2.0:.18e}")

        self.assertGreater(eps, 0.0)
        self.assertGreater(1.0 + eps, 1.0)
        self.assertEqual(1.0 + eps / 2.0, 1.0)

    def test_machine_epsilon_matches_gap_near_one(self):
        print("\n[Test] Machine epsilon vs gap near 1.0")

        eps = machine_epsilon()
        gap_1 = float_gap(1.0)

        print(f"Machine epsilon = {eps:.18e}")
        print(f"Gap near 1.0    = {gap_1:.18e}")

        rel_err = abs(eps - gap_1) / gap_1
        print(f"Relative difference = {rel_err:.3e}")

        self.assertLess(rel_err, 1e-2)


if __name__ == "__main__":
    print("\nRunning CS3430 S26 HW1 Problem 1 unit tests...\n")
    unittest.main(verbosity=2)
    pass
    
    
### Your interpretation comments here inside """ """.

"""
CS3430 HW1 Problem 1 Interpretations:



Unit Test 1: Gap Near 1e10 vs Gap Near 1.0

Results:

    [Test] Gap near 1e10 vs gap near 1.0
    Gap near 1.0  = 2.220446049250313081e-16
    Gap near 1e10 = 1.907348632812500000e-06
    Ratio (1e10 / 1.0) = 8.590e+09

My Interpretation:

    The gap near x = 1.0 is very small, and that is the gap between 1
    and the next representable float after 1.0, which is the machine epsilon.

    The gap near x = 1e10 is much larger than the gap near 1.0 because floating
    point numbers only have a roughtly constant relative precision, not a constant absolute precision.
    This is because of the way floats are represented in memory, with a fixed number of bits for
    the mantissa, and the exponent changes. The same number of bits must represent larger values
    as well as smaller values in the mantissa. As stated in the lecture slides, floating point
    numbers are more densely packed near 0 and more spread out far from 0.

    This relates to the idea of relative vs absolute precision because this function shows 
    the difference between absolute and relative precision. The absolute gap between floating point
    point numbers increases as the number gets larger, but the relative precision stays constant. 

Unit Test 2: Gap Near 1.0

Results:

    [Test] Gap near 1.0
    Computed gap at 1.0      = 2.220446049250313081e-16
    Reference gap (nextafter)= 2.220446049250313081e-16
    Relative error           = 0.000e+00

My Interpretation:

    The gap at 1.0 matches the gap using math.nextafter. This shows me that the float_gap function
    is correctly calculating the gap between 1.0 and the next representable float after 1.0

    The error is basically 0, which shows that the float_gap function is very accurate in finding 
    the gap near 1.0.

Unit Test 3: Machine Epsilon VS Gap Near 1.0

Results:

    [Test] Machine epsilon vs gap near 1.0
    Machine epsilon = 2.220446049250313081e-16
    Gap near 1.0    = 2.220446049250313081e-16
    Relative difference = 0.000e+00

My Interpretation:

    Machine Epsilon and Float Gap at 1.0 are very closely related because they are meassuring the exact same thing in different ways. 
    The machine epsilon is the gap between 1.0 and the next representable float after 1.0. Measuring the float_gap at 1.0 is also 
    finding that same gap. That is why we see the same values. 

    The relative difference is 0, which shows that both functions are measuring the same value accurately.

Unit Test 4: Machine Epsilon Properties

Results:

    [Test] Machine epsilon properties
    Computed machine epsilon = 2.220446049250313081e-16
    1.0 + eps     = 1.000000000000000222e+00
    1.0 + eps/2.0 = 1.000000000000000000e+00

My Interpretation:

    eps/2 becomes smaller than the space near 1.0. So adding it to 1.0 does not change the value of 1.0. 
    It gets rounded off. This is how the loop in the machine_epsilon function actually stops.

    The machine epsilon gives us the gap between 1.0 and the next the smallest representable float after 1.0.
    Therefore, 1.0 + eps moves to the next representable float greater than 1.0, that is why 1.0 + eps is bigger
    than 1.0, because you can actually do 1.0 + eps. However, eps/2 is smaller than the gap between 1.0 and the
    next representable float, so if you take eps/2, and add it to 1.0 eps/2 just gets rounded off. So you are basically
    adding 1.0 to 0, which is why it equals 1.0.

    The machine epsilon relates to the floating point spacing near 1.0, because it is directly measuring that spacing.

"""

