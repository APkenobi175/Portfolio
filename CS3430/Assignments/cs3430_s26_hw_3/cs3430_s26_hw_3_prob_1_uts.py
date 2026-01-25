#############################################################
# cs3430_s26_hw_3_prob_1_uts.py
# Problem 1: Newton-Raphson
# bugs to vladimir kulyukin in canvas
#
# NOTE ON setUpClass():
# ---------------------
#
# In Python's unittest framework, setUpClass() is a special class method that
# runs exactly ONCE before any test methods in that test class are executed.
# I use it here to print a banner (header) so that the unit-test output is
# easier to read. In other words, setUpClass() helps us group related tests
# together (e.g., tests for np_zr1 vs. tests for sp_zr1). Unlike setUp(),
# which runs before EVERY individual test, setUpClass() runs only one time
# per class.
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
##############################################################

import unittest
import numpy as np

from nra import nra, check_zr

class cs3430_s26_hw_3_prob_1_np_zr1_uts(unittest.TestCase):
    """
    Unit tests for nra.np_zr1().

    These tests run Newton-Raphson for a fixed number of iterations using
    NumPy-based numerical evaluation (via SymPy lambdify).
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 1 Unit Tests: np_zr1")
        print("============================================================")

    def test_np_zr1_quadratic_sqrt2_root(self) -> None:
        print("\nSTART: test_np_zr1_quadratic_sqrt2_root")

        text = "x**2 - 2"
        x0 = 1.0
        num_iters = 6

        zr = nra.np_zr1(text, x0, num_iters=num_iters)

        print("  method    = np_zr1")
        print(f"  f(x)      = {text}")
        print(f"  x0        = {x0}")
        print(f"  num_iters = {num_iters}")
        print(f"  zr        = {zr}")
        print(f"  expected  ~ {np.sqrt(2)}")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, np.sqrt(2), atol=1e-4))

        print("PASS !!! test_np_zr1_quadratic_sqrt2_root")

    def test_np_zr1_quadratic_sqrt2_negative_root(self) -> None:
        print("\nSTART: test_np_zr1_quadratic_sqrt2_negative_root")

        text = "x**2 - 2"
        x0 = -1.0
        num_iters = 6

        zr = nra.np_zr1(text, x0, num_iters=num_iters)

        print("  method    = np_zr1")
        print(f"  f(x)      = {text}")
        print(f"  x0        = {x0}")
        print(f"  num_iters = {num_iters}")
        print(f"  zr        = {zr}")
        print(f"  expected  ~ {-np.sqrt(2)}")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, -np.sqrt(2), atol=1e-4))

        print("PASS !!! test_np_zr1_quadratic_sqrt2_negative_root")

    def test_np_zr1_cubic_integer_root(self) -> None:
        print("\nSTART: test_np_zr1_cubic_integer_root")

        text = "x**3 - 1"
        x0 = 0.5
        num_iters = 6

        zr = nra.np_zr1(text, x0, num_iters=num_iters)

        print("  method    = np_zr1")
        print(f"  f(x)      = {text}")
        print(f"  x0        = {x0}")
        print(f"  num_iters = {num_iters}")
        print(f"  zr        = {zr}")
        print("  expected  ~ 1.0")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, 1.0, atol=1e-4))

        print("PASS !!! test_np_zr1_cubic_integer_root")

    def test_np_zr1_cubic_real_root(self) -> None:
        print("\nSTART: test_np_zr1_cubic_real_root")

        text = "x**3 - 2"
        x0 = 2.0
        num_iters = 7
        expected = 2 ** (1 / 3)

        zr = nra.np_zr1(text, x0, num_iters=num_iters)

        print("  method    = np_zr1")
        print(f"  f(x)      = {text}")
        print(f"  x0        = {x0}")
        print(f"  num_iters = {num_iters}")
        print(f"  zr        = {zr}")
        print(f"  expected  ~ {expected}")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, expected, atol=1e-4))

        print("PASS !!! test_np_zr1_cubic_real_root")

    def test_np_zr1_polynomial_with_root_3(self) -> None:
        print("\nSTART: test_np_zr1_polynomial_with_root_3")

        text = "x**2 - x - 6"
        x0 = 4.0
        num_iters = 5

        zr = nra.np_zr1(text, x0, num_iters=num_iters)

        print("  method    = np_zr1")
        print(f"  f(x)      = {text}")
        print(f"  x0        = {x0}")
        print(f"  num_iters = {num_iters}")
        print(f"  zr        = {zr}")
        print("  expected  ~ 3.0")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, 3.0, atol=1e-4))

        print("PASS !!! test_np_zr1_polynomial_with_root_3")


class cs3430_s26_hw_3_prob_1_sp_zr1_uts(unittest.TestCase):
    """
    Unit tests for nra.sp_zr1().

    These tests run Newton-Raphson for a fixed number of iterations using
    SymPy substitution (subs) and symbolic evaluation.
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 1 Unit Tests: sp_zr1")
        print("============================================================")

    def test_sp_zr1_quadratic_sqrt2_root(self) -> None:
        print("\nSTART: test_sp_zr1_quadratic_sqrt2_root")

        text = "x**2 - 2"
        x0 = 1.0
        num_iters = 6

        zr = nra.sp_zr1(text, x0, num_iters=num_iters)

        print("  method    = sp_zr1")
        print(f"  f(x)      = {text}")
        print(f"  x0        = {x0}")
        print(f"  num_iters = {num_iters}")
        print(f"  zr        = {zr}")
        print(f"  expected  ~ {np.sqrt(2)}")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, np.sqrt(2), atol=1e-4))

        print("PASS !!! test_sp_zr1_quadratic_sqrt2_root")

    def test_sp_zr1_quadratic_sqrt2_negative_root(self) -> None:
        print("\nSTART: test_sp_zr1_quadratic_sqrt2_negative_root")

        text = "x**2 - 2"
        x0 = -1.0
        num_iters = 6

        zr = nra.sp_zr1(text, x0, num_iters=num_iters)

        print("  method    = sp_zr1")
        print(f"  f(x)      = {text}")
        print(f"  x0        = {x0}")
        print(f"  num_iters = {num_iters}")
        print(f"  zr        = {zr}")
        print(f"  expected  ~ {-np.sqrt(2)}")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, -np.sqrt(2), atol=1e-4))

        print("PASS !!! test_sp_zr1_quadratic_sqrt2_negative_root")

    def test_sp_zr1_cubic_integer_root(self) -> None:
        print("\nSTART: test_sp_zr1_cubic_integer_root")

        text = "x**3 - 1"
        x0 = 0.5
        num_iters = 6

        zr = nra.sp_zr1(text, x0, num_iters=num_iters)

        print("  method    = sp_zr1")
        print(f"  f(x)      = {text}")
        print(f"  x0        = {x0}")
        print(f"  num_iters = {num_iters}")
        print(f"  zr        = {zr}")
        print("  expected  ~ 1.0")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, 1.0, atol=1e-4))

        print("PASS !!! test_sp_zr1_cubic_integer_root")

    def test_sp_zr1_cubic_real_root(self) -> None:
        print("\nSTART: test_sp_zr1_cubic_real_root")

        text = "x**3 - 2"
        x0 = 2.0
        num_iters = 7
        expected = 2 ** (1 / 3)

        zr = nra.sp_zr1(text, x0, num_iters=num_iters)

        print("  method    = sp_zr1")
        print(f"  f(x)      = {text}")
        print(f"  x0        = {x0}")
        print(f"  num_iters = {num_iters}")
        print(f"  zr        = {zr}")
        print(f"  expected  ~ {expected}")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, expected, atol=1e-4))

        print("PASS !!! test_sp_zr1_cubic_real_root")

    def test_sp_zr1_polynomial_with_root_3(self) -> None:
        print("\nSTART: test_sp_zr1_polynomial_with_root_3")

        text = "x**2 - x - 6"
        x0 = 4.0
        num_iters = 5

        zr = nra.sp_zr1(text, x0, num_iters=num_iters)

        print("  method    = sp_zr1")
        print(f"  f(x)      = {text}")
        print(f"  x0        = {x0}")
        print(f"  num_iters = {num_iters}")
        print(f"  zr        = {zr}")
        print("  expected  ~ 3.0")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, 3.0, atol=1e-4))

        print("PASS !!! test_sp_zr1_polynomial_with_root_3")

class cs3430_s26_hw_3_prob_1_np_zr2_uts(unittest.TestCase):
    """
    Unit tests for nra.np_zr2().

    These tests run Newton-Raphson until the stopping condition is reached:

        abs(x_i - x_{i-1}) <= delta
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 1 Unit Tests: np_zr2")
        print("============================================================")

    def test_np_zr2_quadratic_sqrt2_root(self) -> None:
        print("\nSTART: test_np_zr2_quadratic_sqrt2_root")

        text = "x**2 - 2"
        x0 = 1.0
        delta = 1e-6

        zr = nra.np_zr2(text, x0, delta=delta)

        print("  method   = np_zr2")
        print(f"  f(x)     = {text}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {np.sqrt(2)}")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, np.sqrt(2), atol=1e-4))

        print("PASS !!! test_np_zr2_quadratic_sqrt2_root")

    def test_np_zr2_quadratic_sqrt2_negative_root(self) -> None:
        print("\nSTART: test_np_zr2_quadratic_sqrt2_negative_root")

        text = "x**2 - 2"
        x0 = -1.0
        delta = 1e-6

        zr = nra.np_zr2(text, x0, delta=delta)

        print("  method   = np_zr2")
        print(f"  f(x)     = {text}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {-np.sqrt(2)}")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, -np.sqrt(2), atol=1e-4))

        print("PASS !!! test_np_zr2_quadratic_sqrt2_negative_root")

    def test_np_zr2_cubic_integer_root(self) -> None:
        print("\nSTART: test_np_zr2_cubic_integer_root")

        text = "x**3 - 1"
        x0 = 0.5
        delta = 1e-6

        zr = nra.np_zr2(text, x0, delta=delta)

        print("  method   = np_zr2")
        print(f"  f(x)     = {text}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print("  expected ~ 1.0")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, 1.0, atol=1e-4))

        print("PASS !!! test_np_zr2_cubic_integer_root")

    def test_np_zr2_polynomial_with_root_3(self) -> None:
        print("\nSTART: test_np_zr2_polynomial_with_root_3")

        text = "x**2 - x - 6"
        x0 = 4.0
        delta = 1e-6

        zr = nra.np_zr2(text, x0, delta=delta)

        print("  method   = np_zr2")
        print(f"  f(x)     = {text}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print("  expected ~ 3.0")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, 3.0, atol=1e-4))

        print("PASS !!! test_np_zr2_polynomial_with_root_3")

class cs3430_s26_hw_3_prob_1_sp_zr2_uts(unittest.TestCase):
    """
    Unit tests for nra.sp_zr2().

    These tests run Newton-Raphson until the stopping condition is reached:

        abs(x_i - x_{i-1}) <= delta

    SymPy substitution (subs) is used for evaluation.
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 1 Unit Tests: sp_zr2")
        print("============================================================")

    def test_sp_zr2_quadratic_sqrt2_root(self) -> None:
        print("\nSTART: test_sp_zr2_quadratic_sqrt2_root")

        text = "x**2 - 2"
        x0 = 1.0
        delta = 1e-6

        zr = nra.sp_zr2(text, x0, delta=delta)

        print("  method   = sp_zr2")
        print(f"  f(x)     = {text}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {np.sqrt(2)}")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, np.sqrt(2), atol=1e-4))

        print("PASS !!! test_sp_zr2_quadratic_sqrt2_root")

    def test_sp_zr2_quadratic_sqrt2_negative_root(self) -> None:
        print("\nSTART: test_sp_zr2_quadratic_sqrt2_negative_root")

        text = "x**2 - 2"
        x0 = -1.0
        delta = 1e-6

        zr = nra.sp_zr2(text, x0, delta=delta)

        print("  method   = sp_zr2")
        print(f"  f(x)     = {text}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {-np.sqrt(2)}")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, -np.sqrt(2), atol=1e-4))

        print("PASS !!! test_sp_zr2_quadratic_sqrt2_negative_root")

    def test_sp_zr2_cubic_integer_root(self) -> None:
        print("\nSTART: test_sp_zr2_cubic_integer_root")

        text = "x**3 - 1"
        x0 = 0.5
        delta = 1e-6

        zr = nra.sp_zr2(text, x0, delta=delta)

        print("  method   = sp_zr2")
        print(f"  f(x)     = {text}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print("  expected ~ 1.0")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, 1.0, atol=1e-4))

        print("PASS !!! test_sp_zr2_cubic_integer_root")

    def test_sp_zr2_polynomial_with_root_3(self) -> None:
        print("\nSTART: test_sp_zr2_polynomial_with_root_3")

        text = "x**2 - x - 6"
        x0 = 4.0
        delta = 1e-6

        zr = nra.sp_zr2(text, x0, delta=delta)

        print("  method   = sp_zr2")
        print(f"  f(x)     = {text}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print("  expected ~ 3.0")

        self.assertTrue(check_zr(text, zr))
        self.assertTrue(np.isclose(zr, 3.0, atol=1e-4))

        print("PASS !!! test_sp_zr2_polynomial_with_root_3")

class cs3430_s26_hw_3_prob_1_compute_irrational_sqrt_uts(unittest.TestCase):
    """
    Unit tests for nra.compute_irrational_sqrt().

    This method approximates sqrt(n) by solving:

        x**2 - n = 0

    using Newton-Raphson with a delta stopping condition.
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 1 Unit Tests: compute_irrational_sqrt")
        print("============================================================")

    def test_compute_irrational_sqrt_2(self) -> None:
        print("\nSTART: test_compute_irrational_sqrt_2")

        n = 2
        x0 = 1.0
        delta = 1e-6

        zr = nra.compute_irrational_sqrt(n, x0=x0, delta=delta)

        print("  method   = compute_irrational_sqrt")
        print(f"  n        = {n}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {np.sqrt(n)}")

        self.assertTrue(np.isclose(zr, np.sqrt(n), atol=1e-4))

        print("PASS !!! test_compute_irrational_sqrt_2")

    def test_compute_irrational_sqrt_3(self) -> None:
        print("\nSTART: test_compute_irrational_sqrt_3")

        n = 3
        x0 = 2.0
        delta = 1e-6

        zr = nra.compute_irrational_sqrt(n, x0=x0, delta=delta)

        print("  method   = compute_irrational_sqrt")
        print(f"  n        = {n}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {np.sqrt(n)}")

        self.assertTrue(np.isclose(zr, np.sqrt(n), atol=1e-4))

        print("PASS !!! test_compute_irrational_sqrt_3")

    def test_compute_irrational_sqrt_5(self) -> None:
        print("\nSTART: test_compute_irrational_sqrt_5")

        n = 5
        x0 = 3.0
        delta = 1e-6

        zr = nra.compute_irrational_sqrt(n, x0=x0, delta=delta)

        print("  method   = compute_irrational_sqrt")
        print(f"  n        = {n}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {np.sqrt(n)}")

        self.assertTrue(np.isclose(zr, np.sqrt(n), atol=1e-4))

        print("PASS !!! test_compute_irrational_sqrt_5")

    def test_compute_irrational_sqrt_negative_x0_returns_positive_root(self) -> None:
        print("\nSTART: test_compute_irrational_sqrt_negative_x0_returns_positive_root")

        n = 7
        x0 = -3.0
        delta = 1e-6

        zr = nra.compute_irrational_sqrt(n, x0=x0, delta=delta)

        print("  method   = compute_irrational_sqrt")
        print(f"  n        = {n}")
        print(f"  x0       = {x0} (negative on purpose)")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {np.sqrt(n)}")

        # Confirm the returned result is positive.
        self.assertTrue(zr > 0.0)

        # Confirm it approximates the positive sqrt(n).
        self.assertTrue(np.isclose(zr, np.sqrt(n), atol=1e-4))

        print("PASS !!! test_compute_irrational_sqrt_negative_x0_returns_positive_root")

    def test_compute_irrational_sqrt_perfect_square_raises_value_error(self) -> None:
        print("\nSTART: test_compute_irrational_sqrt_perfect_square_raises_value_error")

        n = 9
        x0 = 1.0
        delta = 1e-6

        print("  method   = compute_irrational_sqrt")
        print(f"  n        = {n} (perfect square)")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print("  expected = ValueError")

        with self.assertRaises(ValueError):
            _ = nra.compute_irrational_sqrt(n, x0=x0, delta=delta)

        print("PASS !!! test_compute_irrational_sqrt_perfect_square_raises_value_error")

class cs3430_s26_hw_3_prob_1_compute_irrational_cubic_root_uts(unittest.TestCase):
    """
    Unit tests for nra.compute_irrational_cubic_root().

    This method approximates cbrt(n) by solving:

        x**3 - n = 0

    using Newton-Raphson with a delta stopping condition.
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 1 Unit Tests: compute_irrational_cubic_root")
        print("============================================================")

    def test_compute_irrational_cubic_root_2(self) -> None:
        print("\nSTART: test_compute_irrational_cubic_root_2")

        n = 2
        x0 = 1.0
        delta = 1e-6

        zr = nra.compute_irrational_cubic_root(n, x0=x0, delta=delta)
        expected = 2 ** (1/3)

        print("  method   = compute_irrational_cubic_root")
        print(f"  n        = {n}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {expected}")

        self.assertTrue(np.isclose(zr, expected, atol=1e-4))

        print("PASS !!! test_compute_irrational_cubic_root_2")

    def test_compute_irrational_cubic_root_5(self) -> None:
        print("\nSTART: test_compute_irrational_cubic_root_5")

        n = 5
        x0 = 2.0
        delta = 1e-6

        zr = nra.compute_irrational_cubic_root(n, x0=x0, delta=delta)
        expected = 5 ** (1/3)

        print("  method   = compute_irrational_cubic_root")
        print(f"  n        = {n}")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {expected}")

        self.assertTrue(np.isclose(zr, expected, atol=1e-4))

        print("PASS !!! test_compute_irrational_cubic_root_5")

    def test_compute_irrational_cubic_root_negative_n(self) -> None:
        print("\nSTART: test_compute_irrational_cubic_root_negative_n")

        n = -7
        x0 = 2.0
        delta = 1e-6

        zr = nra.compute_irrational_cubic_root(n, x0=x0, delta=delta)
        expected = - (abs(n) ** (1/3))

        print("  method   = compute_irrational_cubic_root")
        print(f"  n        = {n} (negative)")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print(f"  zr       = {zr}")
        print(f"  expected ~ {expected}")

        self.assertTrue(zr < 0.0)
        self.assertTrue(np.isclose(zr, expected, atol=1e-4))

        print("PASS !!! test_compute_irrational_cubic_root_negative_n")

    def test_compute_irrational_cubic_root_perfect_cube_raises_value_error(self) -> None:
        print("\nSTART: test_compute_irrational_cubic_root_perfect_cube_raises_value_error")

        n = 27
        x0 = 1.0
        delta = 1e-6

        print("  method   = compute_irrational_cubic_root")
        print(f"  n        = {n} (perfect cube)")
        print(f"  x0       = {x0}")
        print(f"  delta    = {delta}")
        print("  expected = ValueError")

        with self.assertRaises(ValueError):
            _ = nra.compute_irrational_cubic_root(n, x0=x0, delta=delta)

        print("PASS !!! test_compute_irrational_cubic_root_perfect_cube_raises_value_error")
    

if __name__ == "__main__":
    unittest.defaultTestLoader.sortTestMethodsUsing = None
    unittest.main()
