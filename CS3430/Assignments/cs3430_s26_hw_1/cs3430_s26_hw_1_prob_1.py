#############################################################
# cs3430_s26_hw_1_prob_1.py
# solutions to CS3430 S26 HW1 Prob 1
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

def float_gap(x: float) -> float:
    """
    Return the distance to the next representable float greater than x.
    Uses math.nextafter (Python 3.9+).
    """
    nextFloat = math.nextafter(x, math.inf) ## next representable float after x towards +infinity
    return nextFloat - x # the gap near x = 1.0 


def machine_epsilon() -> float:
    """
    Experimentally compute machine epsilon: the smallest eps > 0
    such that 1.0 + eps > 1.0 in floating-point arithmetic.
    """
    eps = 1.0 # init
    while (1.0 + eps / 2.0) > 1.0: 
        eps /= 2.0 # halve eps until 1.0 + eps/2 is not greater than 1.0
    return eps  # final eps is the machine epsilon


def gaps_demo():
    """
    Convenience function (optional) that returns the gaps
    near 1.0 and 1e10, and the machine epsilon.
    """
    gap_1 = float_gap(1.0)
    gap_1e10 = float_gap(1e10)
    eps = machine_epsilon()
    return gap_1, gap_1e10, eps



# Expirement function
print (gaps_demo())

