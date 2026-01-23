#############################################################
# cs3430_s26_hw_2_prob_2.py
# Problem 2: Law of Laminar Flow
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

def sp_laminar_velocity(r: sp.Symbol,
                        R: sp.Symbol,
                        P: sp.Symbol,
                        eta: sp.Symbol,
                        l: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression for the laminar flow velocity function

        v(r) = (P/(4*eta*l)) * (R^2 - r^2),

    where
      - r is the distance from the central axis of the cylindrical tube,
      - R is the tube radius,
      - P is the pressure difference between the two ends of the tube,
      - eta is the viscosity of the fluid (e.g., blood),
      - l is the tube length.

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols.

    Parameters
    ----------
    r : sp.Symbol
        Distance from the axis (0 <= r <= R).
    R : sp.Symbol
        Tube radius (R > 0).
    P : sp.Symbol
        Pressure difference (P can be treated as positive real).
    eta : sp.Symbol
        Fluid viscosity (eta > 0).
    l : sp.Symbol
        Tube length (l > 0).

    Returns
    -------
    sp.Expr
        A SymPy expression representing v(r).
    """
    ### YOUR CODE HERE
    pass

def sp_avg_rate_of_change(r1: sp.Symbol,
                          r2: sp.Symbol,
                          R: sp.Symbol,
                          P: sp.Symbol,
                          eta: sp.Symbol,
                          l: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression for the average rate of change of the
    laminar flow velocity as r moves from r=r1 to r=r2:

        (v(r2) - v(r1)) / (r2 - r1),

    where v(r) is computed by sp_laminar_velocity(r, R, P, eta, l).

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols.

    Parameters
    ----------
    r1 : sp.Symbol
        The starting radius value.
    r2 : sp.Symbol
        The ending radius value.
    R : sp.Symbol
        Tube radius (R > 0).
    P : sp.Symbol
        Pressure difference.
    eta : sp.Symbol
        Fluid viscosity (eta > 0).
    l : sp.Symbol
        Tube length (l > 0).

    Returns
    -------
    sp.Expr
        A SymPy expression representing (v(r2) - v(r1)) / (r2 - r1).
    """
    ### YOUR CODE HERE
    pass

def sp_velocity_gradient(r: sp.Symbol,
                         R: sp.Symbol,
                         P: sp.Symbol,
                         eta: sp.Symbol,
                         l: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression corresponding to the instantaneous rate of change
    of the laminar flow velocity with respect to r:

        velocity gradient = dv/dr.

    The laminar flow velocity is

        v(r) = (P/(4*eta*l)) * (R^2 - r^2),

    computed by sp_laminar_velocity(r, R, P, eta, l).

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols.

    Parameters
    ----------
    r : sp.Symbol
        Distance from the axis (0 <= r <= R).
    R : sp.Symbol
        Tube radius (R > 0).
    P : sp.Symbol
        Pressure difference.
    eta : sp.Symbol
        Fluid viscosity (eta > 0).
    l : sp.Symbol
        Tube length (l > 0).

    Returns
    -------
    sp.Expr
        A SymPy expression representing dv/dr.
    """
    ### YOUR CODE HERE
    pass

def sp_velocity_gradient_closed_form(r: sp.Symbol,
                                     P: sp.Symbol,
                                     eta: sp.Symbol,
                                     l: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression for the closed-form velocity gradient:

        dv/dr = -(P*r)/(2*eta*l).

    This function returns the gradient expression directly (closed form),
    without calling sp.diff().

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols.

    Parameters
    ----------
    r : sp.Symbol
        Distance from the axis (0 <= r <= R).
    P : sp.Symbol
        Pressure difference.
    eta : sp.Symbol
        Fluid viscosity (eta > 0).
    l : sp.Symbol
        Tube length (l > 0).

    Returns
    -------
    sp.Expr
        A SymPy expression representing dv/dr in closed form.
    """
    ### YOUR CODE HERE
    pass

def sp_flow_rate_Q(R: sp.Symbol,
                   P: sp.Symbol,
                   eta: sp.Symbol,
                   l: sp.Symbol) -> sp.Expr:
    """
    Return the SymPy expression for the volumetric flow rate Q predicted by
    Poiseuille's law for laminar flow through a cylindrical tube:

        Q = (pi * P * R^4) / (8 * eta * l).

    This formula is important because it shows that flow rate depends on the
    tube radius as R^4. This means that even a small decrease in radius can
    cause a large decrease in flow.

    In SymPy, an "expression" (sp.Expr) is a symbolic object that represents
    a mathematical formula. It is NOT a numerical value until we substitute
    specific numbers for its symbols.

    Parameters
    ----------
    R : sp.Symbol
        Tube radius (R > 0).
    P : sp.Symbol
        Pressure difference.
    eta : sp.Symbol
        Fluid viscosity (eta > 0).
    l : sp.Symbol
        Tube length (l > 0).

    Returns
    -------
    sp.Expr
        A SymPy expression representing the volumetric flow rate Q.
    """
    ### YOUR CODE HERE
    pass

