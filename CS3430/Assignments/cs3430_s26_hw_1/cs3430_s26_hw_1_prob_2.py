#############################################################
# cs3430_s26_hw_1_prob_2.py
# solutions to CS3430 S26 HW1 Prob 2
# bugs to vladimir kulyukin in canvas
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
##############################################################

import math
from typing import List, Tuple

def g_naive(x: float) -> float:
    """
    Naive implementation of

        g(x) = (1 - cos(x)) / x^2

    This formula is mathematically correct, but numerically unstable
    for very small x due to catastrophic cancellation in (1 - cos(x)).
    """
    gx = (1.0 - math.cos(x)) / (x * x)  # g(x) formula
    return gx
    pass


def g_stable(x: float) -> float:
    """
    Numerically stable reformulation of g(x).

    Uses the trigonometric identity:
        1 - cos(x) = 2 * sin^2(x / 2)

    This avoids subtracting two nearly equal numbers and
    significantly reduces cancellation error for small x.
    """
    return(2.0 * (math.sin(x / 2.0) ** 2) / (x * x))


def g_ref(x: float) -> float:
    """
    Reference approximation for g(x) based on a Taylor expansion
    of cos(x) around x = 0:

        cos(x) = 1 - x^2/2 + x^4/24 - x^6/720 + ...

    Substituting into (1 - cos(x)) / x^2 gives:

        g(x) ≈ 1/2 - x^2/24 + x^4/720

    This approximation is numerically stable for very small x
    and serves as a reference value for error comparison.
    """
    return(0.5 - (x * x) / 24.0 + (x ** 4) / 720.0)
    pass


def compare_errors(xs: List[float]) -> List[Tuple[float, float, float]]:
    """
    For each x in xs, compute absolute errors of g_naive(x)
    and g_stable(x) relative to g_ref(x).

    Returns a list of tuples:
        (x, err_naive, err_stable)

    This convenience function is intended for numerical experiments and
    for observing how cancellation affects accuracy as x -> 0.
    """
    out = []
    for x in xs:
        r = g_ref(x)
        err_naive = abs(g_naive(x) - r)
        err_stable = abs(g_stable(x) - r)
        out.append((x, err_naive, err_stable))
    return out
