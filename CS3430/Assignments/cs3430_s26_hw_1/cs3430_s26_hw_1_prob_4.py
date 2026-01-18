#############################################################
# cs3430_s26_hw_1_prob_4.py
# solutions to CS3430 S26 HW1 Prob 4
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


def central_diff(f, x, h):
    """
    Central divided difference approximation of f'(x):

        f'(x) ≈ (f(x + h) - f(x - h)) / (2h)

    This method has truncation error O(h^2).
    """
    return (f(x + h) - f(x-h)) / (2.0 * h)

def richardson_from_central(f, x, h):
    """
    Richardson extrapolation applied to the central difference.

    Uses:
        R(h) = (4*D(h/2) - D(h)) / 3

    where D(h) is the central difference approximation.
    """
    dh = central_diff(f, x, h)
    dh2 = central_diff(f, x, h / 2.0)
    return (4.0 * dh2 - dh) / 3.0