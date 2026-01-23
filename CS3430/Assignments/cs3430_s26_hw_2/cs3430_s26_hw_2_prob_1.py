#############################################################
# cs3430_s26_hw_2_prob_1_uts.py
# Problem 1: ice cream area limit problem
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


def sp_b(th: sp.Symbol, a: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression corresponding to the base-length function

        b(theta) = 2*a*sin(theta/2)

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols (e.g., theta=0.1, a=2).

    Parameters
    ----------
    th : sp.Symbol
        A SymPy symbol representing theta (assumed positive real).
    a : sp.Symbol
        A SymPy symbol representing a (assumed positive real).

    Returns
    -------
    sp.Expr
        A SymPy expression representing b(theta).
    """
    ### YOUR CODE HERE
    pass


def sp_ice_cream_area(th: sp.Symbol, a: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression corresponding to the ice-cream area formula

        I(theta) = (pi/2) * (b(theta)/2)^2

    where b(theta) is computed by sp_b(th, a).

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols (e.g., theta=0.1, a=2).

    Parameters
    ----------
    th : sp.Symbol
        A SymPy symbol representing theta (assumed positive real).
    a : sp.Symbol
        A SymPy symbol representing a (assumed positive real).

    Returns
    -------
    sp.Expr
        A SymPy expression representing I(theta).
    """
    ### YOUR CODE HERE
    pass

def sp_cone_area(th: sp.Symbol, a: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression corresponding to the cone area formula

        C(theta) = (b(theta)/4) * sqrt(4*a^2 - b(theta)^2)

    where b(theta) is computed by sp_b(th, a).

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols (e.g., theta=0.1, a=2).

    Parameters
    ----------
    th : sp.Symbol
        A SymPy symbol representing theta (assumed positive real).
    a : sp.Symbol
        A SymPy symbol representing a (assumed positive real).

    Returns
    -------
    sp.Expr
        A SymPy expression representing C(theta).
    """
    ### YOUR CODE HERE
    pass

def sp_ice_cream_rat(th: sp.Symbol, a: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression corresponding to the ratio

        Rat(theta) = I(theta) / C(theta)

    where
        I(theta) is computed by sp_ice_cream_area(th, a)
    and
        C(theta) is computed by sp_cone_area(th, a).

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols (e.g., theta=0.1, a=2).

    Parameters
    ----------
    th : sp.Symbol
        A SymPy symbol representing theta (assumed positive real).
    a : sp.Symbol
        A SymPy symbol representing a (assumed positive real).

    Returns
    -------
    sp.Expr
        A SymPy expression representing Rat(theta) = I(theta)/C(theta).
    """
    ### YOUR CODE HERE
    pass

def sp_ice_cream_rat_limit(th: sp.Symbol, a: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression corresponding to the right-hand limit

        L = lim_{theta -> 0+} Rat(theta)

    where
        Rat(theta) = I(theta) / C(theta)
    is computed by sp_ice_cream_rat(theta, a).

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols (e.g., theta=0.1, a=2).

    Parameters
    ----------
    th : sp.Symbol
        A SymPy symbol representing theta (assumed positive real).
    a : sp.Symbol
        A SymPy symbol representing a (assumed positive real).

    Returns
    -------
    sp.Expr
        A SymPy expression representing the right-hand limit as theta -> 0+.
    """
    ### YOUR CODE HERE
    pass




