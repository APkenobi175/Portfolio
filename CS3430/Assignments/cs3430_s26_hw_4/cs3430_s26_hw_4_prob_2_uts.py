#############################################################
# cs3430_s26_hw_4_prob_2_uts.py
# Problem 2: LU Decomposition with Pivoting
#
# Unit tests for lu_decompose_and_solve()
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

from cs3430_s26_hw_4_prob_2 import lu_decompose_and_solve


class cs3430_s26_hw_4_prob_2_lu_uts(unittest.TestCase):
    """
    Unit tests for LU decomposition with pivoting.

    These tests verify:
    1) Structural correctness: P A = L U
    2) Correct application of P^T to b
    3) Correct solution of Ax = b
    4) That SciPy may pivot even when row swaps
       are not mathematically required.
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW4 Problem 2 Unit Tests: LU Decomposition")
        print("============================================================")

    def test_lu_structure_small(self) -> None:
        print("\nSTART: test_lu_structure_small")

        A = np.array([
            [2.0, 1.0],
            [4.0, 3.0]
        ])
        b = np.array([1.0, 2.0])

        P, L, U, x = lu_decompose_and_solve(A, b)

        print("A =\n", A)
        print("P =\n", P)
        print("L =\n", L)
        print("U =\n", U)

        # Structural identity
        self.assertTrue(np.allclose(P @ A, L @ U))

        # Solution correctness
        self.assertTrue(np.allclose(A @ x, b))

        print("PASS !!! test_lu_structure_small")

    def test_lu_solution_matches_numpy(self) -> None:
        print("\nSTART: test_lu_solution_matches_numpy")

        np.random.seed(0)
        A = np.random.randn(5, 5)
        b = np.random.randn(5)

        P, L, U, x = lu_decompose_and_solve(A, b)
        x_np = np.linalg.solve(A, b)

        diff = np.linalg.norm(x - x_np)

        print("||x_student - x_numpy|| =", diff)

        self.assertTrue(np.allclose(x, x_np))
        print("PASS !!! test_lu_solution_matches_numpy")

    def test_lu_requires_pt_b(self) -> None:
        print("\nSTART: test_lu_requires_pt_b")

        # This matrix triggers pivoting
        A = np.array([
            [0.0, 1.0],
            [1.0, 1.0]
        ])
        b = np.array([1.0, 2.0])

        P, L, U, x = lu_decompose_and_solve(A, b)

        print("A =\n", A)
        print("P =\n", P)

        # Verify permutation is not identity
        self.assertFalse(np.allclose(P, np.eye(2)))

        # Verify solution is still correct
        self.assertTrue(np.allclose(A @ x, b))

        print("PASS !!! test_lu_requires_pt_b")

    def test_lu_pivot_even_when_not_strictly_needed(self) -> None:
        print("\nSTART: test_lu_pivot_even_when_not_strictly_needed")

        # Gaussian elimination can proceed without swaps,
        # but SciPy may still pivot for numerical stability.
        A = np.array([
            [1e-12, 1.0],
            [1.0,   1.0]
        ])
        b = np.array([1.0, 2.0])

        P, L, U, x = lu_decompose_and_solve(A, b)

        print("A =\n", A)
        print("P =\n", P)

        # Expect pivoting due to tiny leading entry
        self.assertFalse(np.allclose(P, np.eye(2)))

        self.assertTrue(np.allclose(A @ x, b))

        print("PASS !!! test_lu_pivot_even_when_not_strictly_needed")

    def test_lu_structure_medium_expected_failure(self) -> None:
        """
        This test is EXPECTED to fail.

        It checks whether P @ A == L @ U for a random medium-sized matrix.
        Although this identity holds mathematically, it does NOT reliably
        hold in floating-point arithmetic for random matrices.
        
        NOTE: do NOT try to "fix" this test.
        Instead, observe the failure and learn from it.
        """

        print("\nSTART: test_lu_structure_medium_expected_failure")

        np.random.seed(1)
        A = np.random.randn(10, 10)
        b = np.random.randn(10)

        P, L, U, x = lu_decompose_and_solve(A, b)
        
        residual = np.linalg.norm(P @ A - L @ U)
        scale = np.linalg.norm(A)

        print("||P A - L U|| =", residual)
        print("relative error =", residual / scale)

        # This structural assertion is intentionally too strict
        self.assertTrue(np.allclose(P @ A, L @ U))

    def test_lu_medium_random_system(self) -> None:
        print("\nSTART: test_lu_medium_random_system")

        np.random.seed(1)
        A = np.random.randn(10, 10)
        b = np.random.randn(10)
        
        P, L, U, x = lu_decompose_and_solve(A, b)
        
        # 1) Solution correctness (this is what matters in LU decomposition!)
        self.assertTrue(np.allclose(A @ x, b))
        
        # 2) Structural sanity checks
        self.assertTrue(np.allclose(np.tril(L), L))     # L is lower-triangular
        self.assertTrue(np.allclose(np.triu(U), U))     # U is upper-triangular
        
        # 3) P is a permutation matrix: P x P^T = I; So, P^T = P^-1.
        self.assertTrue(np.allclose(P @ P.T, np.eye(P.shape[0])))
        
        print("PASS !!! test_lu_medium_random_system")


if __name__ == "__main__":
    unittest.defaultTestLoader.sortTestMethodsUsing = None
    unittest.main()
