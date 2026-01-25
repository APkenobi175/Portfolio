#############################################################
# rls.py
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

from __future__ import annotations

import numpy as np

class rls(object):
    """
    Random Linear Systems (RLS).

    This class provides helper methods to generate and solve random linear systems
    of the form:

        A x = b

    where:
    - A is an n x n matrix of reals
    - x is an n x 1 vector (unknown)
    - b is an n x 1 vector (known)
    """

    @staticmethod
    def solve_lin_sys(A: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Solve the linear system A x = b using NumPy.

        Parameters
        ----------
        A : np.ndarray
            A square n x n matrix.
        b : np.ndarray
            A vector of length n (shape (n,) or (n,1)).

        Returns
        -------
        np.ndarray
            The solution vector x.

        Raises
        ------
        ValueError
            If A is not a square matrix or the dimensions of A and b do not match.
        np.linalg.LinAlgError
            If A is singular or the system cannot be solved.
        """
        if A.ndim != 2:
            raise ValueError("A must be a 2D NumPy array.")

        nrows, ncols = A.shape
        if nrows != ncols:
            raise ValueError("A must be square (n x n).")

        if b.ndim not in [1, 2]:
            raise ValueError("b must be a 1D or 2D NumPy array.")

        if b.ndim == 1:
            if b.shape[0] != nrows:
                raise ValueError("Dimension mismatch: b must have length n.")
        else:
            if b.shape != (nrows, 1):
                raise ValueError("Dimension mismatch: b must have shape (n, 1).")

        # Save your solution in rslt computed with np.linalg.solve and return it.
        
        rslt = np.linalg.solve(A, b)

        return rslt

    ### This is a helper method.
    @staticmethod
    def gen_rand_lin_sys(
        n: int,
        lower: float = -10.0,
        upper: float = 10.0,
        seed: int | None = None
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Generate a random linear system A x = b.

        This method generates:
        - A: an n x n matrix of random reals in [lower, upper]
        - b: an n x 1 vector of random reals in [lower, upper]

        Parameters
        ----------
        n : int
            The size of the square matrix A (n x n).
        lower : float
            Lower bound for random values (inclusive).
        upper : float
            Upper bound for random values (inclusive).
        seed : int | None
            If not None, the random seed is fixed for reproducibility.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            A tuple (A, b) where:
            - A has shape (n, n)
            - b has shape (n, 1)

        Raises
        ------
        ValueError
            If n <= 0 or if lower >= upper.
        """
        if n <= 0:
            raise ValueError("n must be a positive integer.")

        if lower >= upper:
            raise ValueError("lower must be < upper.")

        rng = np.random.default_rng(seed)
        A = rng.uniform(lower, upper, size=(n, n))
        b = rng.uniform(lower, upper, size=(n, 1))

        return A, b

    @staticmethod
    def solve_rand_lin_sys(
        n: int,
        lower: float = -10.0,
        upper: float = 10.0,
        seed: int | None = None
    ) -> np.ndarray:
        """
        Generate and solve a random linear system A x = b.

        Parameters
        ----------
        n : int
            The size of the system.
        lower : float
            Lower bound for random values (inclusive).
        upper : float
            Upper bound for random values (inclusive).
        seed : int | None
            If not None, fixes RNG seed for reproducibility.

        Returns
        -------
        np.ndarray
            A solution vector x such that A x ≈ b.
        """
        # 1) Generate a random linear system A x = b of size n.
        #
        # - A is an n x n matrix with random real entries in [lower, upper]
        # - b is an n x 1 column vector with random real entries in [lower, upper]
        #
        # The optional seed argument makes the random system reproducible:
        # if you use the same seed, you will get the same A and b every time.
        A, b = rls.gen_rand_lin_sys(n=n, lower=lower, upper=upper, seed=seed)

        # 2) Solve the generated linear system with rls.solve_lin_sys(A, b) and save
        # the solution  in rslt and return it.
        
        rslt = rls.solve_lin_sys(A, b)
        
        return rslt

    @staticmethod
    def solve_lin_sys_ls(A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray, int, np.ndarray]:
        """
        Solve (or approximately solve) the linear system A x = b using least squares.

        Least squares solves:

            min_x ||Ax - b||_2

        This is useful when:
        - the system is inconsistent (no exact solution exists)
        - the matrix A is singular or ill-conditioned
        - data are noisy ("dirty data")

        NumPy computes the least-squares solution using:

            x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

        Parameters
        ----------
        A : np.ndarray
            An m x n matrix (can be square or rectangular).
        b : np.ndarray
            A vector of shape (m, 1) or (m,).

        Returns
        -------
        tuple[np.ndarray, np.ndarray, int, np.ndarray]
            (x, residuals, rank, s) where:
            - x: the least-squares solution vector (shape (n, 1) or (n,))
            - residuals: how much error is left after fitting
            - rank: rank of A
            - s: singular values of A

        Raises
        ------
        ValueError
            If A or b are not valid NumPy arrays, or if dimensions do not match.
        """
        # A must be a 2D matrix (m x n). If A is not 2D, the linear algebra
        # interpretation of "A x = b" does not make sense.
        if A.ndim != 2:
            raise ValueError("A must be a 2D NumPy array.")

        # b must be either:
        #   - a 1D array of length m      (shape: (m,))
        #   - a 2D column vector (m x 1)  (shape: (m, 1))
        # Anything else is invalid input for this solver.
        if b.ndim not in [1, 2]:
            raise ValueError("b must be a 1D or 2D NumPy array.")

        # m is the number of rows in A. In the system A x = b,
        # b must have m entries to match A.
        m = A.shape[0]

        # If b is 1D, check that its length equals m.
        if b.ndim == 1:
            if b.shape[0] != m:
                raise ValueError("Dimension mismatch: b must have length m.")

        # If b is 2D, check that it has shape (m, 1), i.e., it is a column vector.
        else:
            if b.shape != (m, 1):
                raise ValueError("Dimension mismatch: b must have shape (m, 1).")

        # 1) Compute the least squares solution with NumPy:
        #
        #   minimize ||A x - b||_2
        #
        # You can use np.linalg.lstsq(A, b, rcond=None).
        # This returns:
        #   x         : least-squares solution vector
        #   residuals : how much error remains after fitting
        #   rank      : rank of A (how many independent constraints A contains)
        #   s         : singular values of A (how close A is to collapsing dimension)

        x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

        # 2) Return all four outputs so the caller can inspect not only the solution x
        # but also how well the fit worked (residuals) and how stable A is (rank, s).
        return x, residuals, rank, s

    @staticmethod
    def safe_solve_lin_sys(A: np.ndarray, b: np.ndarray) -> tuple[str, np.ndarray, np.ndarray, int, np.ndarray]:
        """
        Safely solve the linear system A x = b.

        Logic:
        - First, try np.linalg.solve (exact solution, but brittle).
        - If solve fails, fall back to np.linalg.lstsq (least squares, resilient).

        Parameters
        ----------
        A : np.ndarray
            A matrix (usually n x n).
        b : np.ndarray
            A vector of shape (n, 1) or (n,).

        Returns
        -------
        tuple[str, np.ndarray, np.ndarray, int, np.ndarray]
            (method, x, residuals, rank, s) where:

            - method is either "solve" or "lstsq"
            - x is the computed solution (exact or least-squares)
            - residuals is from np.linalg.lstsq (empty if "solve" was used)
            - rank is from np.linalg.lstsq (n if "solve" was used successfully)
            - s is singular values from np.linalg.lstsq (empty if "solve" was used)

        Notes
        -----
        - np.linalg.solve() is brittle: it requires A to be square and invertible.
        - np.linalg.lstsq() is resilient but not as pretty: it always tries to produce the best fit solution
          even when the system is inconsistent, singular, or ill-conditioned.
        """
        # 1) Try solving the system A x = b using the direct solver.
        #
        # This is the "exact" method and is fast and accurate when:
        #   - A is square
        #   - A is invertible (nonsingular)
        #
        # However, np.linalg.solve is brittle: it can fail when A is singular,
        # ill-conditioned, or not square.
        try:
            # 1) Compute x with your solve_lin_sys above.
            
            x = rls.solve_lin_sys(A, b)

            # 2) If solve_lin_sys succeeds, we label the method as "solve".
            #
            # To keep the return format consistent with the least-squares method,
            # we return placeholder values for residuals and singular values.
            method = "solve"
            residuals = np.array([]) # solve() does not return residuals
            rank = int(A.shape[0])   # for a successful square solve, rank is typically n
            s = np.array([])         # solve() does not provide singular values

            return method, x, residuals, rank, s

        # If solve_lin_sys fails (because A is singular, not square, or numerically unstable),
        # we fall back to least squares. Use your implementation of solve_lin_sys_ls(A, b) here.
        except Exception:
            # 3) Compute x, residuals, rank, s with solve_lin_sys_ls(A, b)
            
            x, residuals, rank, s = rls.solve_lin_sys_ls(A, b)
            
            method = "lstsq"
            
            # In the fallback case, we return the full least-squares diagnostic outputs:
            # residuals, rank, and singular values.
            return method, x, residuals, int(rank), s

