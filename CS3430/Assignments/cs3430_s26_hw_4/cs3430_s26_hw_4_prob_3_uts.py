#############################################################
# cs3430_s26_hw_4_prob_3_uts.py
# Problem 3: Archimedes' Method for Computing pi
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
import numpy as np

from cs3430_s26_hw_4_prob_3 import archimedes_pi

class cs3430_s26_hw_4_prob_3_archimedes_uts(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW4 Problem 3 Unit Tests: Archimedes' Method")
        print("============================================================")

    def test_initial_hexagon_bounds(self) -> None:
        print("\nSTART: test_initial_hexagon_bounds")

        n, s6, t6 = archimedes_pi.initial_hexagon()
        pi_lo, pi_hi = archimedes_pi.pi_bounds_from_s_t(n, s6, t6)

        print(f"n = {n}")
        print(f"pi_lower = {pi_lo}")
        print(f"pi_upper = {pi_hi}")

        self.assertEqual(n, 6)
        self.assertTrue(pi_lo < math.pi < pi_hi)

        print("PASS !!! test_initial_hexagon_bounds")

    def test_monotone_squeeze_property(self) -> None:
        print("\nSTART: test_monotone_squeeze_property")

        rows = archimedes_pi.run_table(max_n=1536)

        for i in range(1, len(rows)):
            prev = rows[i - 1]
            curr = rows[i]

            self.assertTrue(curr.pi_lower > prev.pi_lower)
            self.assertTrue(curr.pi_upper < prev.pi_upper)
            self.assertTrue(curr.gap < prev.gap)

        print("PASS !!! test_monotone_squeeze_property")

    def test_pi_enclosure_every_step(self) -> None:
        print("\nSTART: test_pi_enclosure_every_step")

        rows = archimedes_pi.run_table(max_n=3072)

        for r in rows:
            self.assertTrue(r.pi_lower < math.pi < r.pi_upper)

        print("PASS !!! test_pi_enclosure_every_step")

    def test_archimedes_96_gon_bounds(self) -> None:
        print("\nSTART: test_archimedes_96_gon_bounds")

        rows = archimedes_pi.run_table(max_n=96)
        r = rows[-1]

        print(f"n = {r.n}")
        print(f"pi_lower = {r.pi_lower}")
        print(f"pi_upper = {r.pi_upper}")

        # Classic Archimedean bounds (loose numerical form)
        self.assertTrue(r.pi_lower > 3.14)
        self.assertTrue(r.pi_upper < 3.143)

        print("PASS !!! test_archimedes_96_gon_bounds")

    def test_gap_convergence_rate(self) -> None:
        print("\nSTART: test_gap_convergence_rate")

        rows = archimedes_pi.run_table(max_n=12288)

        gaps = [r.gap for r in rows]

        print(f"final gap = {gaps[-1]}")

        # Gap should be very small by 12288 sides
        self.assertTrue(gaps[-1] < 1e-6)

        print("PASS !!! test_gap_convergence_rate")

    def test_archimedes_pi_midpoint_accuracy(self) -> None:
        print("\nSTART: test_archimedes_pi_midpoint_accuracy")

        n = 96
        pi_est = archimedes_pi.archimedes_pi(n)
        pi_ref = math.pi
        error = abs(pi_est - pi_ref)
        
        print(f"n        = {n}")
        print(f"pi_est   = {pi_est}")
        print(f"math.pi = {pi_ref}")
        print(f"|error|  = {error}")
        
        # Archimedes is slow but guaranteed; midpoint should be inside bounds
        self.assertTrue(error < 1e-3)

        print("PASS !!! test_archimedes_pi_midpoint_accuracy")

    def test_print_archimedes_table(self) -> None:
        print("\nSTART: test_print_archimedes_table")

        print("\nArchimedes' Method Table (up to n = 12288):\n")
        archimedes_pi.print_table(max_n=12288)

        print("\nPASS !!! test_print_archimedes_table")

        
        

if __name__ == "__main__":
    unittest.defaultTestLoader.sortTestMethodsUsing = None
    unittest.main()
