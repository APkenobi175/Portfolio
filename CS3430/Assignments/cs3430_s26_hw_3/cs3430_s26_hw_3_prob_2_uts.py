#############################################################
# cs3430_s26_hw_3_prob_2_uts.py
# Problem 2: Random Linear Systems
# bugs to vladimir kulyukin in canvas
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

from rls import rls


class cs3430_s26_hw_3_prob_2_rls_solve_lin_sys_uts(unittest.TestCase):
    """
    Unit tests for rls.solve_lin_sys(A, b).
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 2 Unit Tests: solve_lin_sys")
        print("============================================================")

    def _assert_solution_close(self, A: np.ndarray, x: np.ndarray, b: np.ndarray) -> None:
        """
        Helper: check if A @ x is approximately b.
        """
        # Compute Ax using matrix multiplication.
        # In NumPy, the @ operator performs matrix multiplication.
        Ax = A @ x

        # Verify that x is a correct solution by checking that Ax is close to b.
        #
        # We do NOT expect exact equality due to floating-point rounding error,
        # so we use np.allclose(...) with a small tolerance (atol=1e-6).
        # np.allclose(X, Y, atol=...) returns True if every entry of X is "close enough"
        # to the corresponding entry of Y within a small tolerance.
        #
        # Why do we need this instead of X == Y?
        # Because floating-point arithmetic involves rounding error, so even a correct
        # solution may produce values like 1.00000000001 instead of exactly 1.0.
        #
        # Here atol=1e-6 means we allow an absolute difference of up to 0.000001.
        self.assertTrue(np.allclose(Ax, b, atol=1e-6))

    def test_solve_lin_sys_2x2(self) -> None:
        print("\nSTART: test_solve_lin_sys_2x2")

        # A simple solvable 2x2 system
        A = np.array([[2.0, 1.0],
                      [5.0, 7.0]])
        b = np.array([[11.0],
                      [13.0]])

        x = rls.solve_lin_sys(A, b)

        print("  n = 2")
        print(f"  x.shape = {x.shape}")

        self._assert_solution_close(A, x, b)

        print("PASS !!! test_solve_lin_sys_2x2")

    def test_solve_lin_sys_3x3(self) -> None:
        print("\nSTART: test_solve_lin_sys_3x3")

        A = np.array([[3.0, 2.0, -1.0],
                      [2.0, -2.0, 4.0],
                      [-1.0, 0.5, -1.0]])

        b = np.array([[1.0],
                      [-2.0],
                      [0.0]])

        x = rls.solve_lin_sys(A, b)

        print("  n = 3")
        print(f"  x.shape = {x.shape}")

        self._assert_solution_close(A, x, b)

        print("PASS !!! test_solve_lin_sys_3x3")

    def test_solve_lin_sys_random_10x10(self) -> None:
        print("\nSTART: test_solve_lin_sys_random_10x10")

        n = 10
        A, b = rls.gen_rand_lin_sys(n=n, lower=-5.0, upper=5.0, seed=10)

        x = rls.solve_lin_sys(A, b)

        print(f"  n = {n}")
        print(f"  x.shape = {x.shape}")

        self._assert_solution_close(A, x, b)

        print("PASS !!! test_solve_lin_sys_random_10x10")

    def test_solve_lin_sys_random_100x100(self) -> None:
        print("\nSTART: test_solve_lin_sys_random_100x100")

        n = 100
        A, b = rls.gen_rand_lin_sys(n=n, lower=-2.0, upper=2.0, seed=100)

        x = rls.solve_lin_sys(A, b)

        print(f"  n = {n}")
        print(f"  x.shape = {x.shape}")

        self._assert_solution_close(A, x, b)

        print("PASS !!! test_solve_lin_sys_random_100x100")

    def test_solve_lin_sys_random_500x500(self) -> None:
        print("\nSTART: test_solve_lin_sys_random_500x500")

        n = 500
        A, b = rls.gen_rand_lin_sys(n=n, lower=-1.0, upper=1.0, seed=500)

        x = rls.solve_lin_sys(A, b)

        print(f"  n = {n}")
        print(f"  x.shape = {x.shape}")

        self._assert_solution_close(A, x, b)

        print("PASS !!! test_solve_lin_sys_random_500x500")


class cs3430_s26_hw_3_prob_2_rls_solve_rand_lin_sys_uts(unittest.TestCase):
    """
    Unit tests for rls.solve_rand_lin_sys(n, lower, upper, seed).
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 2 Unit Tests: solve_rand_lin_sys")
        print("============================================================")

    def test_solve_rand_lin_sys_5(self) -> None:
        print("\nSTART: test_solve_rand_lin_sys_5")

        n = 5
        x = rls.solve_rand_lin_sys(n=n, lower=-3.0, upper=3.0, seed=42)

        print(f"  n = {n}")
        print(f"  x.shape = {x.shape}")

        # Verify that the returned solution is a NumPy array.
        #
        # isinstance(obj, ClassName) is a built-in Python function that returns True
        # if obj is an instance (object) of the specified class/type.
        # Here we check that x is an instance of np.ndarray. 
        self.assertTrue(isinstance(x, np.ndarray))

        # Verify that the solution has the expected shape (n, 1),
        # i.e., it is a column vector with n rows.
        self.assertTrue(x.shape == (n, 1))

        print("PASS !!! test_solve_rand_lin_sys_5")

class cs3430_s26_hw_3_prob_2_rls_solve_lin_sys_ls_uts(unittest.TestCase):
    """
    Unit tests for rls.solve_lin_sys_ls(A, b).

    These tests demonstrate that least squares can return a solution even when:
    - the system is inconsistent (no exact solution)
    - A is singular (np.linalg.solve fails)
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 2 Unit Tests: solve_lin_sys_ls")
        print("============================================================")

    def test_solve_lin_sys_ls_exact_solution_exists(self) -> None:
        print("\nSTART: test_solve_lin_sys_ls_exact_solution_exists")

        # Same solvable 2x2 system used in solve_lin_sys tests.
        A = np.array([[2.0, 1.0],
                      [5.0, 7.0]])
        b = np.array([[11.0],
                      [13.0]])

        x, residuals, rank, s = rls.solve_lin_sys_ls(A, b)

        print("  A.shape      =", A.shape)
        print("  b.shape      =", b.shape)
        print("  x.shape      =", x.shape)
        print("  residuals    =", residuals)
        print("  rank         =", rank)
        print("  singular vals=", s)

        # Check that Ax is close to b.
        self.assertTrue(np.allclose(A @ x, b, atol=1e-6))

        print("PASS !!! test_solve_lin_sys_ls_exact_solution_exists")

    def test_solve_lin_sys_ls_inconsistent_system(self) -> None:
        print("\nSTART: test_solve_lin_sys_ls_inconsistent_system")

        # Build a system that is inconsistent by making two identical rows
        # but different b-values, e.g.:
        #
        # x + y = 1
        # x + y = 2   (inconsistent)
        A = np.array([[1.0, 1.0],
                      [1.0, 1.0]])
        b = np.array([[1.0],
                      [2.0]])

        x, residuals, rank, s = rls.solve_lin_sys_ls(A, b)

        print("  A.shape      =", A.shape)
        print("  b.shape      =", b.shape)
        print("  x.shape      =", x.shape)
        print("  residuals    =", residuals)
        print("  rank         =", rank)
        print("  singular vals=", s)

        # Least squares always returns something.
        self.assertTrue(isinstance(x, np.ndarray))
        self.assertTrue(x.shape == (2, 1))

        # For an inconsistent system, Ax won't match b exactly,
        # but the residual norm should still be finite.
        r = (A @ x) - b

        # Compute the Euclidean length (L2 norm) of the residual vector r.
        #
        # np.linalg.norm(r) computes a "size" or "magnitude" of a vector/matrix.
        # For a vector r, the default norm is the L2 norm (Euclidean norm):
        #
        #            ||r||_2 = sqrt(r1^2 + r2^2 + ... + rm^2)
        #
        # In least squares, the residual vector is:
        #            r = Ax - b
        #
        # If ||r||_2 is close to 0, then Ax is very close to b (a good fit).
        # If ||r||_2 is large, then the system is inconsistent/noisy and even the
        # best approximation still has noticeable error.
        # We convert the result to float so that rnorm is a plain Python number.
        rnorm = float(np.linalg.norm(r))
        print("  ||Ax-b||_2   =", rnorm)

        self.assertTrue(rnorm > 0.0)

        print("PASS !!! test_solve_lin_sys_ls_inconsistent_system")

    def test_solve_lin_sys_ls_singular_matrix(self) -> None:
        print("\nSTART: test_solve_lin_sys_ls_singular_matrix")

        # Singular matrix: second row is 2 * first row.
        A = np.array([[1.0, 2.0],
                      [2.0, 4.0]])
        b = np.array([[3.0],
                      [6.0]])

        # np.linalg.solve should fail here because A is singular (not invertible).
        #
        # The keyword "with" below starts a context manager block in Python.
        # In this case, unittest provides a special context manager called
        # assertRaises(...) which checks that the code inside the block raises
        # a specific exception.
        #
        # So this test passes ONLY if rls.solve_lin_sys(A, b) raises LinAlgError.
        # If no error is raised, the test fails.
        with self.assertRaises(np.linalg.LinAlgError):
            # The assignment "_ = ..." means: call the function, but ignore its result.
            #
            # By convention, "_" is used for "a value I don't care about".
            # We do this because the goal here is NOT to use the returned x,
            # but to verify that an exception is raised.
            _ = rls.solve_lin_sys(A, b)

        # least squares should still return a solution.
        x, residuals, rank, s = rls.solve_lin_sys_ls(A, b)

        print("  A.shape      =", A.shape)
        print("  b.shape      =", b.shape)
        print("  x.shape      =", x.shape)
        print("  residuals    =", residuals)
        print("  rank         =", rank)
        print("  singular vals=", s)

        # Check that Ax is still very close to b (this one is consistent).
        self.assertTrue(np.allclose(A @ x, b, atol=1e-6))

        print("PASS !!! test_solve_lin_sys_ls_singular_matrix")

class cs3430_s26_hw_3_prob_2_rls_safe_solve_lin_sys_uts(unittest.TestCase):
    """
    Unit tests for rls.safe_solve_lin_sys(A, b).
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 2 Unit Tests: safe_solve_lin_sys")
        print("============================================================")

    def test_safe_solve_lin_sys_uses_solve_when_possible(self) -> None:
        print("\nSTART: test_safe_solve_lin_sys_uses_solve_when_possible")

        A = np.array([[2.0, 1.0],
                      [5.0, 7.0]])
        b = np.array([[11.0],
                      [13.0]])

        method, x, residuals, rank, s = rls.safe_solve_lin_sys(A, b)

        print("  expected method = solve")
        print("  method          =", method)
        print("  x.shape         =", x.shape)
        print("  residuals       =", residuals)
        print("  rank            =", rank)
        print("  singular vals   =", s)

        # Verify that safe_solve_lin_sys chose the direct (exact) solver.
        self.assertEqual(method, "solve")
        self.assertTrue(np.allclose(A @ x, b, atol=1e-6))

        print("PASS !!! test_safe_solve_lin_sys_uses_solve_when_possible")

    def test_safe_solve_lin_sys_falls_back_to_lstsq_on_singular(self) -> None:
        print("\nSTART: test_safe_solve_lin_sys_falls_back_to_lstsq_on_singular")

        # Singular matrix: second row is 2 * first row.
        A = np.array([[1.0, 2.0],
                      [2.0, 4.0]])
        b = np.array([[3.0],
                      [6.0]])

        method, x, residuals, rank, s = rls.safe_solve_lin_sys(A, b)

        print("  expected method = lstsq")
        print("  method          =", method)
        print("  x.shape         =", x.shape)
        print("  residuals       =", residuals)
        print("  rank            =", rank)
        print("  singular vals   =", s)

        self.assertEqual(method, "lstsq")
        self.assertTrue(np.allclose(A @ x, b, atol=1e-6))

        print("PASS !!! test_safe_solve_lin_sys_falls_back_to_lstsq_on_singular")

    def test_safe_solve_lin_sys_falls_back_to_lstsq_on_inconsistent(self) -> None:
        print("\nSTART: test_safe_solve_lin_sys_falls_back_to_lstsq_on_inconsistent")

        A = np.array([[1.0, 1.0],
                      [1.0, 1.0]])
        b = np.array([[1.0],
                      [2.0]])

        method, x, residuals, rank, s = rls.safe_solve_lin_sys(A, b)

        print("  expected method = lstsq")
        print("  method          =", method)
        print("  x.shape         =", x.shape)
        print("  residuals       =", residuals)
        print("  rank            =", rank)
        print("  singular vals   =", s)

        self.assertEqual(method, "lstsq")

        # The system is inconsistent, so Ax != b, but the result should exist.
        self.assertTrue(isinstance(x, np.ndarray))
        self.assertTrue(x.shape == (2, 1))

        r = (A @ x) - b
        rnorm = float(np.linalg.norm(r))
        print("  ||Ax-b||_2      =", rnorm)

        self.assertTrue(rnorm > 0.0)

        print("PASS !!! test_safe_solve_lin_sys_falls_back_to_lstsq_on_inconsistent")

if __name__ == "__main__":
    unittest.main()
