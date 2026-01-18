#############################################################
# cs3430_s26_hw_1_prob_3.py
# solutions to CS3430 S26 HW1 Prob 3
# bugs to vladimir kulyukin in canvas
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
#############################################################

from typing import List

def naive_sum(xs: List[float]) -> float:
    """
    Naive summation: add numbers in the given order.

    This method is mathematically correct but numerically fragile.
    Floating-point addition is not associative, so the result can
    depend strongly on the order of the inputs.
    """
    s = 0.0
    for x in xs:
        s += x
    return s



def sorted_sum(xs: List[float]) -> float:
    """
    Summation after sorting inputs by increasing magnitude.

    By adding small-magnitude numbers first, this method reduces
    the chance that small values are lost when added to a large
    running total. This often improves numerical accuracy, but
    it is still not optimal in all cases. You can use sorted(xs, key=abs).
    """
    s = 0.0
    for x in sorted(xs, key=abs):
        s += x
    return s



def kahan_sum(xs: List[float]) -> float:
    """
    Kahan compensated summation algorithm.

    This algorithm keeps track of a compensation term that captures
    low-order bits lost during floating-point addition.

    The variable 'c' stores the accumulated rounding error. On each
    iteration, this error is subtracted from the next input value,
    effectively reintroducing previously lost information.

    Kahan summation significantly reduces numerical error in long
    sums and in sums that mix very large and very small values.
    """
    s = 0.0
    c = 0.0  # compensation for lost low-order bits
    for x in xs:
        y = x - c
        t = s + y
        c = (t-s) - y
        s = t
    return s

