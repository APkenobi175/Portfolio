# cs3430_s26_hw_5_prob_2.py
#
# CS3430 S26: Scientific Computing (HW 5, Problem 2)
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
# Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.

from typing import Iterator
from mpmath import mp

def pi_leibniz_mp(*, dps: int = 50) -> Iterator[mp.mpf]:
    """
    Generator for successive approximations of pi using
    the Leibniz series:

        pi / 4 = sum_{k=0}^∞ (-1)^k / (2k + 1)

    This generator yields pi approximations directly by
    multiplying partial sums by 4.

    The purpose of this generator is pedagogical:
      - correctness is trivial,
      - convergence is extremely slow,
      - it serves as a baseline for comparison with Machin.

    Precision is controlled explicitly via mp.dps.
    """
    # Set the working precision for all mpmath operations.
    mp.dps = dps

    # Running partial sum for pi/4.
    s = mp.mpf("0")

    # Alternating sign (+1, -1, +1, -1, ...)
    sign = mp.mpf("1")

    k = 0
    while True:
        # 1) Comput and add the next term of the Leibniz series.
        #
        # Term magnitude shrinks like 1 / (2k+1),
        # which is why convergence is painfully slow. Remember to do mp.mpf(2*k + 1) in
        # the denominator. Your numerator is just sign.
        
        # YOUR CODE HERE.
        s += sign / mp.mpf(2 * k + 1)

        # 2) Yield pi approximation (not pi/4), i.e., mp.mpf("4") * s.

        # YOUR CODE HERE.
        yield mp.mpf("4") * s

        # 3) Flip sign and advance index.
        sign = -sign
        k += 1

# a helper.
def _arctan_series_mp(x: mp.mpf) -> Iterator[mp.mpf]:
    """
    Generator for successive partial sums of arctan(x)
    using the Taylor series:

        arctan(x) = sum_{k=0}^∞ (-1)^k x^(2k+1) / (2k+1)

    This generator yields successive *partial sums*.
    It is used as a building block for Machin's formula.
    """
    s = mp.mpf("0")
    x_power = x            # x^(2k+1), starts at x
    sign = mp.mpf("1")
    k = 0

    while True:
        s += sign * x_power / mp.mpf(2 * k + 1)
        yield s

        # Prepare next power and sign.
        x_power *= x * x   # move from x^(2k+1) to x^(2k+3)
        sign = -sign
        k += 1

def pi_machin_mp(*, dps: int = 50) -> Iterator[mp.mpf]:
    """
    Generator for successive approximations of pi using
    Machin's formula:

        pi / 4 = 4 arctan(1/5) - arctan(1/239)

    This generator yields *pi approximations directly*.

    Key point:
      - uses the same arctan series as Leibniz,
      - but evaluated at small arguments,
      - resulting in dramatically faster convergence.

    Precision is controlled explicitly via mp.dps.
    """
    # 1) Set precision
    mp.dps = dps

    one = mp.mpf("1")

    # 2) Generators for the two arctan series.
    # define two generators g1 that does _arctan_series_mp(one/mp.mpf("5"))
    # and g2 that does _arctan_series_mp(one / mp.mpf("239")). Save them
    # in variables g1 and g2, respectively.
    
    # YOUR CODE HERE.
    g1 = _arctan_series_mp(one / mp.mpf("5"))
    g2 = _arctan_series_mp(one / mp.mpf("239"))

    while True:
        # 1) Pull one more term from each arctan generator.
        a = next(g1)
        b = next(g2)

        # 2) Assemble Machin's identity and yield pi.
        yield mp.mpf("4") * (mp.mpf("4") * a - b)
