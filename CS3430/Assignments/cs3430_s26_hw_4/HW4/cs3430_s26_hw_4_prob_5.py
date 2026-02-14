#############################################################
# cs3430_s26_hw_4_prob_5.py
# Problem 5: Image Deblurring via LU Decomposition (1D, row-wise)
#
# Copyright (C) Vladimir Kulyukin.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, USU.
#############################################################

import numpy as np
from scipy.linalg import lu

from cs3430_s26_hw_4_prob_1 import forward_substitution, back_substitution

def build_blur_matrix_1d(n: int, alpha: float, beta: float) -> np.ndarray:
    """
    Build an n x n tridiagonal blur matrix for 1D blurring.

    The model is:
        b_i = alpha * x_{i-1} + beta * x_i + alpha * x_{i+1}

    Boundary pixels use only available neighbors.
    """
    if n <= 0:
        raise ValueError("n must be positive")

    A = np.zeros((n, n), dtype=float)

    for i in range(n):
        A[i, i] = beta
        if i - 1 >= 0:
            A[i, i - 1] = alpha
        if i + 1 < n:
            A[i, i + 1] = alpha

    return A


def blur_row(row: np.ndarray, alpha: float, beta: float) -> np.ndarray:
    """
    Apply 1D blur to a single row using the tridiagonal model.
    """
    n = row.size
    A = build_blur_matrix_1d(n, alpha, beta)
    return A @ row


def deblur_row_lu(row_blurred: np.ndarray,
                  alpha: float,
                  beta: float) -> np.ndarray:
    """
    Deblur a single row using LU decomposition.

    Solves:
        A x = b

    where A is the blur matrix, b is the blurred row, x is
    x is the deblurred row.
    """
    n = row_blurred.size
    A = build_blur_matrix_1d(n, alpha, beta)

    # 1) LU decomposition with pivoting
    # Obtain P, L, U with lu(A)

    P, L, U = lu(A)

    # 2) Compute b_tilde as the product of P^T and row_blurred.

    b_tilde = P.T @ row_blurred
    
    # 3) Forward + back substitution
    # Use yoru implementations to compute y and x.
    y = forward_substitution(L, b_tilde)
    x = back_substitution(U, y)

    return x

### These are helper functions.
def blur_image_rows(image: np.ndarray,
                    alpha: float,
                    beta: float) -> np.ndarray:
    """
    Apply 1D blur to each row of a grayscale image.
    """
    if image.ndim != 2:
        raise ValueError("image must be a 2D array")

    blurred = np.zeros_like(image, dtype=float)

    for r in range(image.shape[0]):
        blurred[r, :] = blur_row(image[r, :], alpha, beta)

    return blurred


def deblur_image_rows(image_blurred: np.ndarray,
                      alpha: float,
                      beta: float) -> np.ndarray:
    """
    Deblur each row of a grayscale image using LU decomposition.
    """
    if image_blurred.ndim != 2:
        raise ValueError("image must be a 2D array")

    deblurred = np.zeros_like(image_blurred, dtype=float)

    for r in range(image_blurred.shape[0]):
        deblurred[r, :] = deblur_row_lu(image_blurred[r, :], alpha, beta)

    return deblurred
