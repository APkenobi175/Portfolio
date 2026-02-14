#############################################################
# cs3430_s26_hw_4_prob_4.py
# Problem 4: Related Rates and Pi Approximation
#
# Copyright (C) Vladimir Kulyukin.
# For personal study by students enrolled in
# CS3430 S26: Scientific Computing, USU.
#############################################################

from typing import Callable
import sympy as sp

def cone_water_level_rate(
    R: float,
    H: float,
    dV_dt: float,
    h_value: float,
    pi_value: float
) -> float:
    """
    Compute the rate of change of water height dh/dt in an inverted
    conical tank using related rates.

    Parameters
    ----------
    R : float
        Radius of the cone at the top (meters)
    H : float
        Height of the cone (meters)
    dV_dt : float
        Rate of change of volume (m^3 / min)
    h_value : float
        Current water height (meters)
    pi_value : float
        Numerical value of pi to use (e.g., math.pi or Archimedes approximation)

    Returns
    -------
    float
        dh/dt at h = h_value
    """

    # 1) Define SymPy symbol variables
    h, t = sp.symbols('h t', positive=True)

    # 2) Compute r as a function of R, H, and h (similar triangles)
    
    r = (R / H) * h
    
    # 3) Compute volume of water V as a function of pi_value, r, and h

    V = (1/3) * pi_value * r**2 * h

    # 4) Differentiate volume of water V with respect to h
    # Hint: use sp.diff(V, h) to compute dV_dh.

    dV_dh = sp.diff(V, h)

    # 5) Related rates: dV/dt = (dV/dh)(dh/dt)
    # We compute the SymPy expression
    dh_dt_expr = dV_dt / dV_dh

    # 6) Substitute numeric value of h (i.e., h_value) to compute
    # dh_dt_value. You can use dt_dt_expr.subs(h, h_value)

    dh_dt_value = dh_dt_expr.subs(h, h_value)

    return float(dh_dt_value)
