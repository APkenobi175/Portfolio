#############################################################
# cs3430_s26_hw_4_prob_2.py
# Problem 2: LU Decomposition with Pivoting
#
# Copyright (C) Vladimir Kulyukin.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
#############################################################

from typing import Tuple
import numpy as np
from scipy.linalg import lu

from cs3430_s26_hw_4_prob_1 import (
    forward_substitution,
    back_substitution,
)


def lu_decompose_and_solve(
    A: np.ndarray,
    b: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Perform LU decomposition with pivoting and solve Ax = b.

    This method follows exactly the algorithm presented in Lecture 6:

        1) Compute A = P L U using SciPy.
        2) Apply the permutation to the right-hand side: b_tilde = P^T b.
        3) Solve L y = b_tilde using forward substitution.
        4) Solve U x = y using back substitution.

    Parameters
    ----------
    A : np.ndarray
        An n x n coefficient matrix.
    b : np.ndarray
        A right-hand side vector of length n.

    Returns
    -------
    P : np.ndarray
        The permutation matrix.
    L : np.ndarray
        The lower-triangular matrix.
    U : np.ndarray
        The upper-triangular matrix.
    x : np.ndarray
        The solution to Ax = b.

    Raises
    ------
    ValueError
        If A is not square or if dimensions of A and b do not match.
    """

    # -------------------------------
    # Step 1: LU decomposition
    # -------------------------------
    # Obtain P, L, and U with lu(A)

    # YOUR CODE HERE.
    # 1a. Check if A is square and dimensions match with b
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix A must be square.")
    n = A.shape[0]
    if b.shape != (n,):
        raise ValueError("Vector b must have compatible dimensions with A.")
    # 1b. Perform LU decomposition with pivoting
    P, L, U = lu(A)

    # -------------------------------
    # Step 2: Reorder the right-hand side
    # (SciPy uses A = P L U)
    # -------------------------------
    # Compute b_tilde as the product of P^T and b.
    # P^T is computed with P.T in numpy.

    # YOUR CODE HERE.
    # 2a. Compute b_tilde
    b_tilde = P.T @ b
    
    # -------------------------------
    # Step 3: Forward substitution
    # Solve L y = b_tilde
    # -------------------------------
    # Solve for y with your forward_substitution implementation.

    # YOUR CODE HERE.
    # 3a. Compute y
    y = forward_substitution(L, b_tilde)

    # -------------------------------
    # Step 4: Back substitution
    # Solve U x = y
    # -------------------------------
    # Solve for x with your back_substitution implementation.
    
    # 4a. Compute x
    x = back_substitution(U, y)

    return P, L, U, x

    

