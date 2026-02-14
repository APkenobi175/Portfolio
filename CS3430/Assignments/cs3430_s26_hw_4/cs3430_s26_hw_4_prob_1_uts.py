#############################################################
# cs3430_s26_hw_4_prob_1_uts.py
# Problem 1: Forward and Back Substitution
# bugs to vladimir kulyukin in canvas
#
# Copyright (C) Vladimir Kulyukin.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
#############################################################

import unittest
import numpy as np

from cs3430_s26_hw_4_prob_1 import (
    forward_substitution,
    back_substitution
)

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def random_lower_triangular(n: int) -> np.ndarray:
    """
    Generate a random n x n lower-triangular matrix suitable for
    testing forward substitution.

    The matrix is constructed by:
      1) Generating an n x n matrix with entries drawn from a
         standard normal distribution using np.random.randn.
      2) Zeroing out all entries above the main diagonal using
         np.tril, leaving a lower-triangular matrix.
      3) Adjusting diagonal entries that are too close to zero.

    Why the diagonal adjustment?
      - Forward substitution requires division by a_ii.
      - Zero or near-zero pivots would cause division by zero
        or severe numerical instability.
      - If |a_ii| < 0.5, we shift it away from zero while
        preserving its sign.

    This guarantees:
      - No zero pivots (the algorithm can run),
      - But still allows poor conditioning, which is important
        for observing floating-point error propagation.

    Note:
      Random lower-triangular matrices generated this way may be
      poorly conditioned, especially near the top-left corner.
      This is intentional and helps illustrate numerical behavior
      discussed in Lecture 6.
    """
    L = np.tril(np.random.randn(n, n))
    for i in range(n):
        if abs(L[i, i]) < 0.5:
            L[i, i] += np.sign(L[i, i]) + 1.0
    return L


def random_upper_triangular(n: int) -> np.ndarray:
    """
    Generate a random n x n upper-triangular matrix suitable for
    testing back substitution.

    The matrix is constructed by:
      1) Generating an n x n matrix with entries drawn from a
         standard normal distribution using np.random.randn.
      2) Zeroing out all entries below the main diagonal using
         np.triu, leaving an upper-triangular matrix.
      3) Adjusting diagonal entries that are too close to zero.

    Why the diagonal adjustment?
      - Back substitution requires division by a_ii.
      - Zero or near-zero pivots would cause division by zero
        or excessive amplification of rounding error.
      - If |a_ii| < 0.5, we shift it away from zero.

    Compared to random lower-triangular matrices, small pivots in
    upper-triangular matrices tend to appear closer to the top-left
    corner, which means they are encountered later during the
    back-substitution process.

    This often limits how far amplified rounding error can propagate,
    which is why back substitution may exhibit smaller accumulated
    numerical error in large systems.
    """
    U = np.triu(np.random.randn(n, n))
    for i in range(n):
        if abs(U[i, i]) < 0.5:
            U[i, i] += np.sign(U[i, i]) + 1.0
    return U


# ============================================================
# Forward Substitution Tests
# ============================================================

class cs3430_s26_hw_4_prob_1_forward_substitution_uts(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW4 Problem 1 Unit Tests: forward_substitution")
        print("============================================================")

    def test_forward_substitution_numeric_small(self) -> None:
        print("\nSTART: test_forward_substitution_numeric_small")

        np.random.seed(0)
        n = 3
        L = random_lower_triangular(n)
        b = np.random.randn(n)

        y = forward_substitution(L, b)
        y_ref = np.linalg.solve(L, b)

        print("L =\n", L)
        print("b =", b)
        print("y (student) =", y)
        print("y (numpy)   =", y_ref)

        self.assertTrue(np.allclose(y, y_ref, atol=1e-10))

        print("PASS !!! test_forward_substitution_numeric_small")

    def test_forward_substitution_numeric_medium(self) -> None:
        print("\nSTART: test_forward_substitution_numeric_medium")

        np.random.seed(1)
        n = 8
        L = random_lower_triangular(n)
        b = np.random.randn(n)

        y = forward_substitution(L, b)
        y_ref = np.linalg.solve(L, b)

        self.assertTrue(np.allclose(y, y_ref, atol=1e-10))

        print("PASS !!! test_forward_substitution_numeric_medium")

    def test_forward_substitution_numeric_large(self) -> None:
        print("\nSTART: test_forward_substitution_numeric_large")

        np.random.seed(42)
        n = 50
        L = random_lower_triangular(n)
        b = np.random.randn(n)
        
        y = forward_substitution(L, b)
        y_ref = np.linalg.solve(L, b)
        
        err = np.linalg.norm(y - y_ref)
        
        print(f"matrix size = {n} x {n}")
        print(f"||y_student - y_numpy|| = {err}")
        
        self.assertTrue(np.allclose(y, y_ref, atol=1e-10))
        
        print("PASS !!! test_forward_substitution_numeric_large")

    def test_forward_substitution_zero_pivot_raises(self) -> None:
        print("\nSTART: test_forward_substitution_zero_pivot_raises")

        L = np.array([
            [1.0, 0.0],
            [2.0, 0.0]
        ])
        b = np.array([1.0, 1.0])

        print("L =\n", L)
        print("b =", b)
        print("expected = ValueError")

        with self.assertRaises(ValueError):
            _ = forward_substitution(L, b)

        print("PASS !!! test_forward_substitution_zero_pivot_raises")

    def test_forward_substitution_bad_shape_raises(self) -> None:
        print("\nSTART: test_forward_substitution_bad_shape_raises")

        L = np.eye(3)
        b = np.ones(4)

        print("L shape =", L.shape)
        print("b shape =", b.shape)
        print("expected = ValueError")

        with self.assertRaises(ValueError):
            _ = forward_substitution(L, b)

        print("PASS !!! test_forward_substitution_bad_shape_raises")


# ============================================================
# Back Substitution Tests
# ============================================================

class cs3430_s26_hw_4_prob_1_back_substitution_uts(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW4 Problem 1 Unit Tests: back_substitution")
        print("============================================================")

    def test_back_substitution_numeric_small(self) -> None:
        print("\nSTART: test_back_substitution_numeric_small")

        np.random.seed(2)
        n = 3
        U = random_upper_triangular(n)
        b = np.random.randn(n)

        x = back_substitution(U, b)
        x_ref = np.linalg.solve(U, b)

        print("U =\n", U)
        print("b =", b)
        print("x (student) =", x)
        print("x (numpy)   =", x_ref)

        self.assertTrue(np.allclose(x, x_ref, atol=1e-10))

        print("PASS !!! test_back_substitution_numeric_small")

    def test_back_substitution_numeric_medium(self) -> None:
        print("\nSTART: test_back_substitution_numeric_medium")

        np.random.seed(3)
        n = 8
        U = random_upper_triangular(n)
        b = np.random.randn(n)

        x = back_substitution(U, b)
        x_ref = np.linalg.solve(U, b)

        self.assertTrue(np.allclose(x, x_ref, atol=1e-10))

        print("PASS !!! test_back_substitution_numeric_medium")

    def test_back_substitution_zero_pivot_raises(self) -> None:
        print("\nSTART: test_back_substitution_zero_pivot_raises")

        U = np.array([
            [1.0, 2.0],
            [0.0, 0.0]
        ])
        b = np.array([1.0, 1.0])

        print("U =\n", U)
        print("b =", b)
        print("expected = ValueError")

        with self.assertRaises(ValueError):
            _ = back_substitution(U, b)

        print("PASS !!! test_back_substitution_zero_pivot_raises")


    def test_back_substitution_numeric_large(self) -> None:
        print("\nSTART: test_back_substitution_numeric_large")

        np.random.seed(43)
        n = 50
        U = random_upper_triangular(n)
        b = np.random.randn(n)
        
        x = back_substitution(U, b)
        x_ref = np.linalg.solve(U, b)
        
        err = np.linalg.norm(x - x_ref)
        
        print(f"matrix size = {n} x {n}")
        print(f"||x_student - x_numpy|| = {err}")
        
        self.assertTrue(np.allclose(x, x_ref, atol=1e-10))
        
        print("PASS !!! test_back_substitution_numeric_large")

    def test_back_substitution_bad_shape_raises(self) -> None:
        print("\nSTART: test_back_substitution_bad_shape_raises")

        U = np.eye(3)
        b = np.ones(2)

        print("U shape =", U.shape)
        print("b shape =", b.shape)
        print("expected = ValueError")

        with self.assertRaises(ValueError):
            _ = back_substitution(U, b)

        print("PASS !!! test_back_substitution_bad_shape_raises")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    unittest.defaultTestLoader.sortTestMethodsUsing = None
    unittest.main()
