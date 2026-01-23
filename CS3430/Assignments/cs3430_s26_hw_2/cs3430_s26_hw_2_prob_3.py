#############################################################
# cs3430_s26_hw_2_prob_2.py
# Problem 2: Variable Brightness Stars
# bugs to vladimir kulyukin in canvas
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
##############################################################

import sympy as sp
from typing import Callable, Union
import numpy as np

def sp_to_np(expr: sp.Expr) -> Callable[..., Union[float, np.ndarray]]:
    """
    Convert a SymPy expression into a callable Python function
    using SymPy's lambdify (NumPy backend).

    Parameters
    ----------
    expr : sp.Expr
        A SymPy expression (e.g., 2*a*sin(theta/2)).

    Returns
    -------
    Callable[..., Union[float, np.ndarray]]
        A NumPy-aware Python function produced by lambdify.
        It can be evaluated on either Python floats or NumPy arrays.
    """
    vars_sorted = sorted(list(expr.free_symbols), key=lambda s: s.name)
    return sp.utilities.lambdify(vars_sorted, expr, modules="numpy")

def sp_cepheid_brightness(t: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression for the brightness model of the Cepheid variable
    star Delta Cephei:

        B(t) = 4.0 + 0.35*sin((2*pi*t)/5.4)

    where:
      - t is time measured in days,
      - 4.0 is the average brightness,
      - 0.35 is the brightness amplitude,
      - 5.4 is the period (days) between maximum brightness values.

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols (e.g., t=1.0).

    Parameters
    ----------
    t : sp.Symbol
        A SymPy symbol representing time (in days).

    Returns
    -------
    sp.Expr
        A SymPy expression representing B(t).
    """
    ### YOUR CODE HERE
    pass

def sp_cepheid_brightness_rate(t: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression for the rate of change of the brightness
    model of the Cepheid variable star Delta Cephei.

    If the brightness is modeled by

        B(t) = 4.0 + 0.35*sin((2*pi*t)/5.4),

    then the rate of change is the derivative

        dB/dt.

    In SymPy, we compute derivatives symbolically using sp.diff.

    Parameters
    ----------
    t : sp.Symbol
        A SymPy symbol representing time (in days).

    Returns
    -------
    sp.Expr
        A SymPy expression representing dB/dt.
    """
    ### YOUR CODE HERE
    pass

def np_cepheid_brightness(t_vals: np.ndarray) -> np.ndarray:
    """
    Evaluate the Cepheid brightness model B(t) over a NumPy array of time values.

    This function demonstrates how SymPy and NumPy can work together:

      1) Build a symbolic model B(t) in SymPy (sp_cepheid_brightness)
      2) Convert the symbolic expression to a NumPy-aware function (sp_to_np)
      3) Evaluate that function on an array of t-values

    Parameters
    ----------
    t_vals : np.ndarray
        A NumPy array of time values (in days), e.g., produced by np.linspace.

    Returns
    -------
    np.ndarray
        A NumPy array containing brightness values B(t_vals[i]) for each i.
    """
    ### YOUR CODE HERE
    pass

def plot_cepheid_brightness(t_start: float, t_end: float, n: int):
    """
    Plot the Cepheid brightness model B(t) over a time interval.

    IMPORTANT:
    This function returns the matplotlib Figure object so that unit tests
    (or other code) can save the plot reliably.

    Parameters
    ----------
    t_start : float
        Start time in days.
    t_end : float
        End time in days.
    n : int
        Number of sample points.

    Returns
    -------
    matplotlib.figure.Figure
        The matplotlib Figure containing the plot.
    """
    import matplotlib.pyplot as plt

    t_vals = np.linspace(t_start, t_end, n)
    b_vals = np_cepheid_brightness(t_vals)

    fig = plt.figure()
    plt.plot(t_vals, b_vals)
    plt.xlabel("t (days)")
    plt.ylabel("Brightness B(t)")
    plt.title(f"Cepheid Brightness Model from t={t_start} to t={t_end} days")
    plt.grid(True)
    plt.tight_layout()

    return fig

