#############################################################
# cs3430_s26_hw_4_prob_4_uts.py
# Problem 4: Related Rates in a Conical Tank
#
# Copyright (C) Vladimir Kulyukin.
# For personal study by students enrolled in
# CS3430 S26: Scientific Computing, USU.
#############################################################

import unittest
import math
import numpy as np

from cs3430_s26_hw_4_prob_3 import archimedes_pi
from cs3430_s26_hw_4_prob_4 import cone_water_level_rate

class cs3430_s26_hw_4_prob_4_uts(unittest.TestCase):
    """
    Unit tests for Problem 4: Related rates in an inverted conical tank.

    These tests compare results obtained using:
    - math.pi
    - Archimedes' approximation to pi
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW4 Problem 4 Unit Tests: Related Rates")
        print("============================================================")

    def test_cone_rate_using_math_pi(self) -> None:
        print("\nSTART: test_cone_rate_using_math_pi")

        R = 2.0          # meters
        H = 4.0          # meters
        dV_dt = 2.0      # m^3 / min
        h = 3.0          # meters

        dh_dt = cone_water_level_rate(
            R=R,
            H=H,
            dV_dt=dV_dt,
            h_value=h,
            pi_value=math.pi
        )

        print(f"Using math.pi")
        print(f"dh/dt = {dh_dt} m/min")

        self.assertTrue(dh_dt > 0.0)

        print("PASS !!! test_cone_rate_using_math_pi")

    def test_cone_rate_using_archimedes_pi(self) -> None:
        print("\nSTART: test_cone_rate_using_archimedes_pi")

        R = 2.0
        H = 4.0
        dV_dt = 2.0
        h = 3.0
        n = 96

        pi_arch = archimedes_pi.archimedes_pi(n)

        dh_dt = cone_water_level_rate(
            R=R,
            H=H,
            dV_dt=dV_dt,
            h_value=h,
            pi_value=pi_arch
        )

        print(f"Using Archimedes pi (n = {n})")
        print(f"pi ≈ {pi_arch}")
        print(f"dh/dt = {dh_dt} m/min")

        self.assertTrue(dh_dt > 0.0)

        print("PASS !!! test_cone_rate_using_archimedes_pi")

    def test_math_pi_vs_archimedes_pi_difference(self) -> None:
        print("\nSTART: test_math_pi_vs_archimedes_pi_difference")

        R = 2.0
        H = 4.0
        dV_dt = 2.0
        h = 3.0
        n = 96

        dh_dt_math = cone_water_level_rate(
            R, H, dV_dt, h, math.pi
        )

        dh_dt_arch = cone_water_level_rate(
            R, H, dV_dt, h, archimedes_pi.archimedes_pi(n)
        )

        diff = abs(dh_dt_math - dh_dt_arch)

        print(f"dh/dt (math.pi)       = {dh_dt_math}")
        print(f"dh/dt (Archimedes pi) = {dh_dt_arch}")
        print(f"|difference|          = {diff}")

        self.assertTrue(diff < 1e-3)

        print("PASS !!! test_math_pi_vs_archimedes_pi_difference")


    def test_cone_rate_using_archimedes_pi_2(self) -> None:
        print("\nSTART: test_cone_rate_using_archimedes_pi_2")

        R = 3.0
        H = 5.0
        dV_dt = 3.0
        h = 4.0
        n = 96

        pi_arch = archimedes_pi.archimedes_pi(n)

        dh_dt = cone_water_level_rate(
            R=R,
            H=H,
            dV_dt=dV_dt,
            h_value=h,
            pi_value=pi_arch
        )

        print(f"Using Archimedes pi (n = {n})")
        print(f"pi ≈ {pi_arch}")
        print(f"dh/dt = {dh_dt} m/min")

        self.assertTrue(dh_dt > 0.0)

        print("PASS !!! test_cone_rate_using_archimedes_pi_2")

    def test_math_pi_vs_archimedes_pi_difference_2(self) -> None:
        print("\nSTART: test_math_pi_vs_archimedes_pi_difference_2")

        R = 3.0
        H = 5.0
        dV_dt = 3.0
        h = 4.0
        n = 96

        dh_dt_math = cone_water_level_rate(
            R, H, dV_dt, h, math.pi
        )

        dh_dt_arch = cone_water_level_rate(
            R, H, dV_dt, h, archimedes_pi.archimedes_pi(n)
        )

        diff = abs(dh_dt_math - dh_dt_arch)

        print(f"dh/dt (math.pi)       = {dh_dt_math}")
        print(f"dh/dt (Archimedes pi) = {dh_dt_arch}")
        print(f"|difference|          = {diff}")

        self.assertTrue(diff < 1e-3)

        print("PASS !!! test_math_pi_vs_archimedes_pi_difference_2")        


if __name__ == "__main__":
    unittest.defaultTestLoader.sortTestMethodsUsing = None
    unittest.main()
