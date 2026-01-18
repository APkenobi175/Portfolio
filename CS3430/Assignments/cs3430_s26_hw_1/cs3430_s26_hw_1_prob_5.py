#############################################################
# cs3430_s26_hw_1_prob_5.py
# solutions to CS3430 S26 HW1 Prob 5
# bugs to vladimir kulyukin in canvas
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
#############################################################

import numpy as np
import sympy as sp
import math


def trap(f, a, b, n):
    """
    Composite trapezoidal rule for numerical integration.

    Approximates:
        integral_a^b f(x) dx

    using n subintervals.
    """
    h = (b - a) / n
    x = a + h * np.arange(n + 1)
    y = f(x)
    return (h / 2.0) * (y[0] + 2.0 * np.sum(y[1:-1]) + y[-1])


def romberg(f, a, b, K=5):
    """
    Romberg integration using Richardson extrapolation.

    Builds a (K+1) x (K+1) Romberg table R where:
        R[k,0] = trapezoidal rule with 2^k subintervals
        R[k,j] = Richardson extrapolation of R[k,j-1]

    Returns the full Romberg table.
    """
    R = np.zeros((K + 1, K + 1), dtype=float)

    for i in range (K+1):
        n = 2**i
        R[i,0] = trap(f, a, b, n)

        for j in range(1, i + 1):
            R[i, j] = R[i, j - 1] + (R[i, j - 1] - R[i - 1, j - 1]) / (4 ** j - 1)
    return R


def print_romberg_table(R):
    """
    Function to print the full Romberg Table
    """
    rows, cols = R.shape
    for i in range(rows):
        line = []
        for j in range(i + 1):
            line.append(f"{R[i,j]: .16e}")
        print(" | ".join(line))

def integral_pi_romberg(x: np.ndarray) -> np.ndarray:
    return 4.0 / (1.0 + x ** 2) # Intragand for functiont o compute pi


################################
# Pi Expirement
################################
print("PI Expirement (PART C)")
a, b = 0.0, 1.0
R = romberg(integral_pi_romberg, a, b, K=6)
print_romberg_table(R)
best = R[6, 6]
bestErr = abs(best - math.pi)
trapEstimate = R[6, 0]
trapErr = abs(trapEstimate - math.pi)

print(f"Python Math Pi: {math.pi: .16e}")

print(f"Trapezoidal Estimate: {trapEstimate: .16e}, Error: {trapErr: .3e}")
print(f"Romberg Estimate: {best: .16e}, Error: {bestErr: .3e}")

print(f"Romberg is {trapErr / bestErr: .3e} times more accurate than Trapezoidal")

################################
# Symbolic Reference With SymPy
################################

import sympy as sp

x0 = 5 # evaluate the derivative at x = 5

x = sp.Symbol('x', real =True)

expression = 4 / (1 + x**2)

diffExpression = sp.diff(expression, x)

diffExpressionToNumpy = sp.lambdify(x, diffExpression, "numpy")

val = float(diffExpressionToNumpy(x0))

print("\n(PART D) Sympy derivative of 4/(x^2 + 1):")

print("f(x) =", expression)
print("f'(x) =", diffExpression)
print(f"f'({x0}) =", val)


