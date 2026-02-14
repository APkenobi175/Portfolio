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



#############################################################
#                    Problem 1 Writeup:                     #
#                     By: Ammon Phipps                      #
#############################################################

'''
Observations from forward and back substitution unit tests:

I ran the unit tests for both forward and back substitution, and
found that both the back substitution and forward substitution all 
passed successfully without any errors.

Both the forward and back substition implementations created results
that closely matched Numpy's built-in linear solver results. However, I also 
notice that depending on the size of the matrix, the the accuracy of the results
varied slightly. Smaller matricies matched numpy exactly, while larger matricies
started to drift slightly from the numpy results. 

FORWARD SUBSTITUTION:

For example, in the forward substitution tests, for a small matrix of size 3x3, the results

    y (student) = [  0.23275868  -0.20215907 -11.65033252]
    y (numpy)   = [  0.23275868  -0.20215907 -11.65033252]

My results matched numpy result's exactly. However, for a larger matrix of size 50x50, the results were:

    ||y_student - y_numpy|| = 0.30828178832687153

Which demonstrates a small but noticable difference between my function and numpys results. 


BACK SUBSTITUTION:

In the back substitiution tests, for a small matrix of size 3x3, the results were:

    x (student) = [13.19104419  0.70942864 -2.16664607]
    x (numpy)   = [13.19104419  0.70942864 -2.16664607]'
    
Which again, just like in forward substitution, matched numpy's results exactly, However,
Again, for a larger matrix of size 50x50, the results were:

    ||x_student - x_numpy|| = 1.705548350035669e-07

This result is incredibly small, which means the difference in my implementation and numpy's could come 
down to errors in floating point precision. This is significantly smaller than the result in forward substitution.


My Explanations:

1. Numerical Stability and Error Propagation:
    Both forward and back substitution methods involve calculations where each step depends on the previous ones.
    In forward substitution, errors can accumulate more significantly because each computed value is used in all subsequent calculations.
    This is why in the larger matrices my error was much bigger than the error in back substitution.

    In back substitution, while errors can still accumulate, the structure of upper-triangular matrices will lead to less propagation of errors, because
    each computed value is used in fewer calculations, so theres less opportunity for the errors to build up.


2. Floating Point Precision:

    Both Numpy and my implementations use floating-point arithmetic, which has precision limitations. So, despite both methods being mathematically fantastic,
    this is computer science, not pure math, so the limitations of floating point arithmetic can lead to small errors. Especially if the methods are different
    e.g numpy vs my implementation.

In Conclusion I believe that the differences in accuracy between forward, and back substitution, and the differences in mine and numpy's results are 
to be expected and does not mean there are any bugs or errors in the code itself. 

'''




import numpy as np

def forward_substitution(
    L: np.ndarray,
    b: np.ndarray
) -> np.ndarray:
    """
    Solve Ly = b for y, where L is a lower-triangular matrix.

    Parameters
    ----------
    L : np.ndarray
        Lower-triangular matrix of shape (n, n).
    b : np.ndarray
        Right-hand side vector of shape (n,).

    Returns
    -------
    np.ndarray
        Solution vector y of shape (n,).

    Raises
    ------
    ValueError
        If dimensions are incompatible or a zero pivot is encountered.
    """
    n = L.shape[0]

    if L.shape != (n, n):
        raise ValueError("L must be a square matrix.")
    if b.shape != (n,):
        raise ValueError("b must be a vector of compatible dimension.")

    y = np.zeros(n, dtype=float)

    ### YOUR CODE HERE
    # For each row in the matrix L
    for i in range(n):
        # 1. Check for zero pivot, if found raise an error
        if abs(L[i, i]) < 1e-12:
            raise ValueError(f"Zero or NEAR zero pivot encountered at row {i}")
        # 2. Intialize sum for the dot product
        sum_Ly = 0.0
        # 3. Compute the dot product of the i-th row of L and the vector y
        for j in range(i):
            sum_Ly += L[i, j] * y[j]
        # 4. Compute the i-th component of the solution vector y
        y[i] = (b[i] - sum_Ly) / L[i, i]

    return y

import numpy as np

def back_substitution(
    U: np.ndarray,
    b: np.ndarray
) -> np.ndarray:
    """
    Solve Ux = b for x, where U is an upper-triangular matrix.

    Parameters
    ----------
    U : np.ndarray
        Upper-triangular matrix of shape (n, n).
    b : np.ndarray
        Right-hand side vector of shape (n,).

    Returns
    -------
    np.ndarray
        Solution vector x of shape (n,).

    Raises
    ------
    ValueError
        If dimensions are incompatible or a zero pivot is encountered.
    """
    n = U.shape[0]

    if U.shape != (n, n):
        raise ValueError("U must be a square matrix.")
    if b.shape != (n,):
        raise ValueError("b must be a vector of compatible dimension.")

    x = np.zeros(n, dtype=float)

    ### YOUR CODE HERE
    # For each row in the matrix U, starting from the last row going upwards
    for i in range(n - 1, -1, -1):
        # 1. Check for zero pivot, if found raise an error
        if abs(U[i, i]) < 1e-12:
            raise ValueError(f"Zero or NEAR zero pivot encountered at row {i}")
        # 2. Intialize sum for the dot product
        sum_Ux = 0.0
        # 3. Compute the dot product of the i-th row of U and the vector x
        for j in range(i + 1, n):
            sum_Ux += U[i, j] * x[j]
        # 4. Compute the i-th component of the solution vector x
        x[i] = (b[i] - sum_Ux) / U[i, i]
    
    return x
