#############################################################
# nra.py
# Problem 1: Newton-Raphson
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
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

### this is a utility function
def check_zr(text: str, zr: float) -> bool:
    """
    Check whether a given float value is a good approximation of a zero root
    of the polynomial represented by `text`.
        
    Parameters
    ----------
    text : str
    A string representation of a polynomial in x.
    zr : float
    A candidate zero root approximation.
        
    Returns
    -------
    bool
    True if f(zr) is sufficiently close to 0.0; otherwise False.
    """
    x, f = nra._parse_poly(text)
    # f_np is a NumPy function built out of SymPy expression.
    f_np = sp.lambdify(x, f, modules="numpy")
    return np.allclose(float(f_np(float(zr))), 0.0)

class nra(object):
    """
    Newton-Raphson Algorithm (NRA) utilities for approximating zero roots
    of polynomial functions.
    """

    @staticmethod
    def _parse_poly(text: str) -> tuple[sp.Symbol, sp.Expr]:
        """
        Parse a polynomial function represented as a string into a SymPy expression.

        The input string must be a valid Python/SymPy expression using:
        - x as the variable name
        - ** for exponentiation

        Example
        -------
        text = "x**2 - 2*x + 1"

        Parameters
        ----------
        text : str
            A string representation of a polynomial in x.

        Returns
        -------
        tuple[sp.Symbol, sp.Expr]
            A pair (x, f) where:
            - x is the SymPy symbol for the variable
            - f is the SymPy expression representing the polynomial
        """
        x = sp.Symbol("x")
        # I use parse_expr(text, ...) below. It converts the string "text" into a SymPy expression (sp.Expr).
        # Example: if text = "x**2 - 2", then f becomes the symbolic expression f(x) = x**2 - 2.
        #
        # The argument local_dict={"x": x} tells SymPy that the name "x" appearing in the text
        # should be treated as the SymPy symbol x (e.g., x = sp.Symbol("x")).
        #
        # Once f is a SymPy expression, we can do symbolic math with it, e.g.:
        #   sp.diff(f, x)      -> symbolic derivative f'(x)
        #   f.subs(x, 1.5)     -> substitute x=1.5 into the expression
        f = parse_expr(text, local_dict={"x": x})
        return x, f

    @staticmethod
    def np_zr1(text: str, x0: float, num_iters: int = 3) -> float:
        """
        Approximate a zero root of a polynomial using the Newton-Raphson algorithm
        for a fixed number of iterations.

        The Newton-Raphson update rule is:

            x_i = x_{i-1} - f(x_{i-1}) / f'(x_{i-1})

        This method runs exactly `num_iters` iterations and returns x_num_iters.

        SymPy is used to parse and differentiate the polynomial symbolically.
        NumPy is used to evaluate the iteration numerically.

        Parameters
        ----------
        text : str
            A string representation of a polynomial in x.
        x0 : float
            The initial guess for the zero root.
        num_iters : int
            The number of Newton-Raphson iterations to perform.

        Returns
        -------
        float
            The final Newton-Raphson approximation after `num_iters` iterations.

        Raises
        ------
        ZeroDivisionError
            If the derivative f'(x_i) is (numerically) close to 0 during iteration.
        """
        x, f = nra._parse_poly(text)
        df = sp.diff(f, x)

        f_np = sp.lambdify(x, f, modules="numpy")        
        df_np = sp.lambdify(x, df, modules="numpy")

        # We start Newton-Raphson at the initial guess x0.
        # We convert x0 to a float to ensure we are doing *numerical* computation
        # (not symbolic computation) inside this NumPy-based method.        
        xi = float(x0)

        for _ in range(num_iters):
            # 1) Evaluate the function f(x) at the current guess xi.
            # f_np is a NumPy-compatible function (created earlier via lambdify),
            # so f_np(xi) returns a numeric value that we convert to float.
            # In my comments below, I assume that you will save this float in fxi
            
            # 1. 
            fxi = float(f_np(xi))



            # 2) Evaluate the derivative f'(x) at the current guess xi.
            # df_np is a NumPy-compatible derivative function.
            # This value tells us how steep the curve is at xi.
            # I assume that you will save this float in dfxi.
            
            dfxi = float(df_np(xi))

            # 3) Newton-Raphson requires division by f'(xi).
            # If f'(xi) is 0 (or extremely close to 0), then the update step
            # would cause a division-by-zero error or a numerically unstable jump.
            # In that case, we stop and raise an exception.
            if np.isclose(dfxi, 0.0):
                raise ZeroDivisionError(
                    f"Newton-Raphson failed: derivative is ~0 at x={xi}"
                )

            # 4) compute the new value of xi from the current xi, fxi, and dfxi.
            xi = xi - fxi / dfxi

        # 5) return xi
        return float(xi)

    @staticmethod
    def sp_zr1(text: str, x0: float, num_iters: int = 3) -> float:
        """
        Approximate a zero root of a polynomial using the Newton-Raphson algorithm
        for a fixed number of iterations, using SymPy for both symbolic work and
        numeric evaluation.

        The Newton-Raphson update rule is:

            x_i = x_{i-1} - f(x_{i-1}) / f'(x_{i-1})

        This method runs exactly `num_iters` iterations and returns x_num_iters.

        Parameters
        ----------
        text : str
            A string representation of a polynomial in x.
        x0 : float
            The initial guess for the zero root.
        num_iters : int
            The number of Newton-Raphson iterations to perform.

        Returns
        -------
        float
            The final Newton-Raphson approximation after `num_iters` iterations.

        Raises
        ------
        ZeroDivisionError
            If the derivative f'(x_i) is (numerically) close to 0 during iteration.
        """

        # 1) We parse the polynomial text into a SymPy expression.
        # The helper method _parse_poly(text) returns:
        #   - x: the SymPy symbol representing the variable (e.g., x = sp.Symbol("x"))
        #   - f: the SymPy expression representing the polynomial (e.g., x**2 - 2)
        x, f = nra._parse_poly(text)

        # 2) Compute the symbolic derivative f'(x) using SymPy.
        # SymPy can differentiate expressions exactly and symbolically.
        # I assume that you will save it in df.
        
        df = sp.diff(f, x)

        # 3) Convert the initial guess x0 into a SymPy Float so that subsequent
        # Newton-Raphson iterations are carried out in SymPy's numeric system.
        # (This keeps everything as SymPy objects instead of Python floats.)
        xi = sp.Float(x0)

        # Repeat the Newton-Raphson update rule a fixed number of times.
        for _ in range(num_iters):

            # 1) Evaluate f(x) at the current guess xi using SymPy substitution.
            # subs(x, xi) replaces every occurrence of x in the symbolic expression
            # with the current numeric value xi.
            # I assume you will save this in fxi
            
            fxi = f.subs(x, xi) # fxi using substitution

            # 2) Evaluate f'(x) at the current guess xi, also using substitution.
            # I assume you will save this in dfxi
            
            dfxi = df.subs(x, xi) # dfxi using substitution

            # 3) Convert the derivative value to a Python float so we can run a
            # numerical near-zero check. (np.isclose expects numeric values.)
            dfxi_f = float(dfxi) 

            # 4) If the derivative is 0 (or extremely close to 0), then the Newton
            # update would require division by ~0, which is numerically unstable.
            # In that case, we stop and raise an exception.
            if np.isclose(dfxi_f, 0.0):
                raise ZeroDivisionError(
                    f"Newton-Raphson failed: derivative is ~0 at x={float(xi)}"
                )

            # 5) Core Newton-Raphson update formula (done symbolically/numerically
            # inside SymPy):
            #
            #   x_{i} = x_{i-1} - f(x_{i-1}) / f'(x_{i-1})
            #
            # Geometrically, this computes the x-intercept of the tangent line
            # to f(x) at the current guess xi.
            # Compute with xi, fxi, and dfxi you have saved above.
            
            xi = xi - fxi / dfxi

        # 6) return xi.
        return float(xi)

    @staticmethod
    def np_zr2(text: str, x0: float, delta: float = 0.0001) -> float:
        """
        Approximate a zero root of a polynomial using the Newton-Raphson algorithm
        until the absolute difference between consecutive approximations is <= delta.

        The Newton-Raphson update rule is:

            x_i = x_{i-1} - f(x_{i-1}) / f'(x_{i-1})

        This method repeatedly applies the update rule until:

            abs(x_i - x_{i-1}) <= delta

        SymPy is used to parse and differentiate the polynomial symbolically.
        NumPy is used to evaluate the iteration numerically.

        Parameters
        ----------
        text : str
            A string representation of a polynomial in x.
        x0 : float
            The initial guess for the zero root.
        delta : float
            The maximum allowed absolute difference between successive guesses.

        Returns
        -------
        float
            The final Newton-Raphson approximation when convergence is reached.

        Raises
        ------
        ZeroDivisionError
            If the derivative f'(x_i) is (numerically) close to 0 during iteration.
        """
        # 1) Parse the polynomial text into a SymPy expression f(x).
        # The helper method returns:
        #   - x: the SymPy symbol representing the variable
        #   - f: the SymPy expression representing the polynomial
        x, f = nra._parse_poly(text)

        # 2) Compute the symbolic derivative f'(x) using SymPy.
        df = sp.diff(f, x)

        # 3) Convert the symbolic expressions f(x) and f'(x) into fast NumPy-callable
        # Python functions. After lambdify:
        #
        #   f_np(val)   computes f(val) numerically
        #   df_np(val)  computes f'(val) numerically
        #
        # This allows us to run Newton-Raphson efficiently using floats.
        f_np = sp.lambdify(x, f, modules="numpy")
        df_np = sp.lambdify(x, df, modules="numpy")

        # 4) Initialize the iteration with the starting guess x0 (numeric float).
        x_prev = float(x0)

        # 5) Run Newton-Raphson until we meet the stopping condition:
        #   |x_next - x_prev| <= delta
        # which means consecutive approximations are close enough.
        while True:

            # 5.1) Evaluate f(x_prev) numerically with f_np and save it in f_prev.
            f_prev = float(f_np(x_prev))

            # 5.2) Evaluate f'(x_prev) numerically with df_np and save it in
            # df_prev
            df_prev = float(df_np(x_prev))

            # Newton-Raphson requires dividing by f'(x_prev).
            # If the derivative is 0 or extremely close to 0, the update step
            # would be a division-by-zero (or a numerically unstable jump).
            if np.isclose(df_prev, 0.0):
                raise ZeroDivisionError(
                    f"Newton-Raphson failed: derivative is ~0 at x={x_prev}"
                )

            # 5.3) Compute the next Newton-Raphson approximation:
            #
            #   x_next = x_prev - f(x_prev) / f'(x_prev)
            #
            # Each iteration typically moves x closer to a zero root of f(x).
            x_next = x_prev - f_prev / df_prev

            # 5.4) Stopping condition: if the new approximation is close enough to the
            # previous one, we assume the algorithm has converged.
            if abs(x_next - x_prev) <= delta:
                return float(x_next)

            # 5.5) Otherwise, keep iterating: the next guess becomes the previous guess.
            x_prev = x_next
    
    @staticmethod
    def sp_zr2(text: str, x0: float, delta: float = 0.0001) -> float:
        """
        Approximate a zero root of a polynomial using the Newton-Raphson algorithm
        until the absolute difference between consecutive approximations is <= delta,
        using SymPy symbolic evaluation via substitution (subs).

        The Newton-Raphson update rule is:

            x_i = x_{i-1} - f(x_{i-1}) / f'(x_{i-1})

        This method repeatedly applies the update rule until:

            abs(x_i - x_{i-1}) <= delta

        Parameters
        ----------
        text : str
            A string representation of a polynomial in x.
        x0 : float
            The initial guess for the zero root.
        delta : float
            The maximum allowed absolute difference between successive guesses.

        Returns
        -------
        float
            The final Newton-Raphson approximation when convergence is reached.

        Raises
        ------
        ZeroDivisionError
            If the derivative f'(x_i) is (numerically) close to 0 during iteration.
        """
        # 1) Parse the polynomial text into a SymPy expression f(x).
        # This returns:
        #   - x: a SymPy symbol representing the variable
        #   - f: a SymPy expression representing the polynomial
        x, f = nra._parse_poly(text)

        # 2) Compute the symbolic derivative f'(x).
        df = sp.diff(f, x)

        # 3) Initialize the starting guess as a SymPy Float.
        # This ensures the Newton-Raphson computations below are carried out
        # using SymPy's numeric objects (instead of Python floats).
        x_prev = sp.Float(x0)

        # 4) Keep iterating until the stopping condition is met.
        # Stopping condition:
        #   |x_next - x_prev| <= delta
        # meaning two consecutive approximations are sufficiently close.
        while True:

            # 4.1) Evaluate f(x_prev) by substituting x = x_prev into the symbolic
            # expression f. This produces a SymPy numeric value with f.subs(x, x_prev)
            # Save your result in f_prev.
            
            f_prev = f.subs(x, x_prev)

            # 4.2) Evaluate f'(x_prev) by substituting x = x_prev into df with df.subs(x, x_prev)
            # and save your result in df_prev.
            
            df_prev = df.subs(x, x_prev)

            # 4.3) Newton-Raphson requires dividing by f'(x_prev).
            # If the derivative is 0 (or extremely close to 0), the update step
            # would require division by ~0, which is numerically unstable.
            # We convert df_prev to float so np.isclose can do a numeric check.
            if np.isclose(float(df_prev), 0.0):
                raise ZeroDivisionError(
                    f"Newton-Raphson failed: derivative is ~0 at x={float(x_prev)}"
                )

            # 4.4) Compute the next Newton-Raphson approximation using the formula:
            #
            #   x_next = x_prev - f(x_prev) / f'(x_prev)
            #
            # Since f_prev and df_prev are SymPy values, this update step also
            # stays in SymPy's numeric domain.
            
            x_next = x_prev - f_prev / df_prev

            # 4.5) Check whether Newton-Raphson has converged:
            # if the update step is smaller than delta, we stop.
            #
            # We convert the SymPy difference to float so we can compare it to delta.
            if abs(float(x_next - x_prev)) <= delta:
                return float(x_next)

            # 4.6) Otherwise, continue iterating: shift x_prev forward.
            x_prev = x_next

    @staticmethod
    def compute_irrational_sqrt(n: int, x0: float = 1.0, delta: float = 0.0001) -> float:
        """
        Approximate sqrt(n) by applying Newton-Raphson to the polynomial:

            f(x) = x**2 - n

        This method reuses nra.np_zr2().

        Parameters
        ----------
        n : int
            A positive integer that is not a perfect square.
        x0 : float
            An initial guess for sqrt(n).
        delta : float
            Stopping threshold: stop when abs(x_i - x_{i-1}) <= delta.

        Returns
        -------
        float
            A floating-point approximation to sqrt(n).

        Raises
        ------
        ValueError
            If n <= 0 or n is a perfect square.

        Notes
        -----
        This method assumes:

        1) You want the positive square root.

        2) The starting guess x0 is reasonable and not near 0.

        If we pass x0 < 0, Newton may converge to the negative root of x**2 - n.
        That is not "wrong" mathematically, but for sqrt(n) we typically want
        the positive root. Therefore, we take abs(x0) before running Newton-Raphson.
        """
        # 1) For square roots, we assume n is a positive integer.
        # sqrt(n) is only defined for n > 0 in the real numbers.
        if n <= 0:
            raise ValueError("n must be a positive integer.")

        # 2) If n is a perfect square (e.g., 1, 4, 9, 16, ...),
        # then sqrt(n) is a rational number and does not illustrate
        # the "irrational approximation" idea we want here.
        # We detect perfect squares by checking whether:
        #   (int(sqrt(n)))^2 == n
        if int(np.sqrt(n)) ** 2 == n:
            raise ValueError(f"n={n} is a perfect square; sqrt({n}) is rational.")

        # 3) Convert the starting guess x0 to a positive float.
        # This method assumes we want the POSITIVE square root of n.
        # If x0 were negative, Newton-Raphson might converge to the negative root.
        x0 = abs(float(x0))

        # 4) Build the polynomial whose zero root is sqrt(n):
        #
        #   x^2 - n = 0   =>   x = ±sqrt(n)
        #
        # We represent the polynomial as a text string because our NRA methods
        # take polynomial strings as input. Save your str representation in poly_text.
        
        poly_text = f"x**2 - ({n})"

        # 5) Reuse our existing Newton-Raphson "delta stopping condition" method np_zr2.
        # This repeatedly applies NRA until two consecutive approximations differ
        # by at most delta. Save your result in rslt and return it.
        
        rslt = nra.np_zr2(poly_text, x0, delta)
        
        return rslt

    @staticmethod
    def compute_irrational_cubic_root(n: int, x0: float = 1.0, delta: float = 0.0001) -> float:
        """
        Approximate the real cube root of n using the Newton-Raphson algorithm (NRA).

        We approximate cbrt(n) as the real zero root of the polynomial:

            f(x) = x**3 - n

        This method reuses nra.np_zr2().

        Parameters
        ----------
        n : int
            A nonzero integer that is not a perfect cube.
        x0 : float
            An initial guess for cbrt(n).
        delta : float
            Stopping threshold: stop when abs(x_i - x_{i-1}) <= delta.

        Returns
        -------
        float
            A floating-point approximation to the real cube root of n.

        Raises
        ------
        ValueError
            If n == 0 or n is a perfect cube.

        Notes
        -----
        This method returns the real cube root of n.

        If n < 0, the real cube root is negative. Therefore, we preserve the sign
        of the initial guess x0 by making sure x0 has the same sign as n.
        """
        # 1) For cubic roots, n cannot be 0 because cbrt(0) = 0 is trivial.
        # We want students to approximate a NONTRIVIAL irrational cube root.
        if n == 0:
            raise ValueError("n must be nonzero.")

        # 2) Check whether n is a perfect cube (e.g., 1, 8, 27, 64, ...).
        # If n is a perfect cube, then cbrt(n) is rational, which is not the
        # point of this method.
        #
        # We handle both positive and negative n by working with abs(n).
        # We estimate the integer cube root using round(abs(n)^(1/3)) and check:
        #   cube_root_int^3 == abs(n)
        cube_root_int = int(round(abs(n) ** (1 / 3)))
        if cube_root_int ** 3 == abs(n):
            raise ValueError(f"n={n} is a perfect cube; cbrt({n}) is rational.")

        # 3) Convert the initial guess to a float so Newton-Raphson runs numerically.
        x0 = float(x0)

        # 4) Keep the sign of the initial guess consistent with the sign of n.
        #
        # Why does this matter?
        # For x^3 - n = 0, there is exactly one real cube root:
        #   - if n > 0, the real root is positive
        #   - if n < 0, the real root is negative
        #
        # Newton-Raphson tends to converge more reliably when the starting guess
        # has the same sign as the real root.
        if n > 0:
            x0 = abs(x0)
        else:
            x0 = -abs(x0)

        # 5) Build the polynomial whose zero root is cbrt(n):
        #
        #   x^3 - n = 0   =>   x = cbrt(n)
        #
        # Parentheses around n handle negative values cleanly in the text.
        poly_text = f"x**3 - ({n})"

        # 6) Reuse the existing Newton-Raphson method that stops when consecutive
        # approximations differ by at most delta (np_zr2). Save your result in rslt
        # and return it.
        
        rslt = nra.np_zr2(poly_text, x0, delta)
        
        return rslt


