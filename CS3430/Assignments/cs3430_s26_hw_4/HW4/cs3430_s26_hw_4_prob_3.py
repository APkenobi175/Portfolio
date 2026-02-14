#############################################################
# cs3430_s26_hw_4_prob_3.py
# Problem 3: Archimedes' Method of Computing pi
# bugs to vladimir kulyukin in canvas
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
##############################################################


#############################################################
#                    Problem 3 Writeup:                     #
#                     By: Ammon Phipps                      #
#############################################################



'''
Observations from Archimedes' Method Unit Tests:

I ran the unit tests for Archimedes' method for computing pi, and
found that all tests passed successfully without any errors.

This is the results table I got from the Unit Test:


     n        pi_lower        pi_upper              gap
------------------------------------------------------------
     6  3.000000000000  3.464101615138 4.641016151378e-01
    12  3.105828541230  3.215390309173 1.095617679432e-01
    24  3.132628613281  3.159659942098 2.703132881627e-02
    48  3.139350203047  3.146086215131 6.736012084595e-03
    96  3.141031950891  3.142714599646 1.682648755044e-03
   192  3.141452472285  3.141873049980 4.205776945216e-04
   384  3.141557607912  3.141662747055 1.051391434461e-04
   768  3.141583892149  3.141610176600 2.628445058583e-05
  1536  3.141590463237  3.141597034323 6.571086575313e-06
  3072  3.141592106043  3.141593748817 1.642773807653e-06
  6144  3.141592516588  3.141592927874 4.112854785632e-07
 12288  3.141592618641  3.141592725623 1.069818020838e-07

The test results confirmed important things about the Archimedes' method:

1. The squeeze property: As n increases, the lower bound on pi increases
   and the upper bound decreases. The bounds never cross and pi always lives
   in between them.

2. The gap between the upper and lower bounds also decreases as n increases, showing 
    that we are converging to the real value of pi.

3. The convergance is relatively slow, even when N doubles each iteration, our gap is not
   shrinking very fast. However, even though its slow, its still stable and doesn't overshoot 
   pi, pi is always somewhere within lower and upper bounds.

'''

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import List, Tuple
import math

@dataclass(frozen=True)
class ArchimedesRow:
    """
    One iteration row for Archimedes' pi-bounding table.

    Attributes:
        n: number of polygon sides.
        pi_lower: lower bound on pi from inscribed n-gon.
        pi_upper: upper bound on pi from circumscribed n-gon.
        gap: pi_upper - pi_lower.
    """
    n: int
    pi_lower: float
    pi_upper: float
    gap: float


class archimedes_pi:
    """
    Archimedes' method for bounding pi by inscribed/circumscribed polygons
    on the unit circle (radius = 1).

    Notation (unit circle):
        s_n: side length (chord) of inscribed regular n-gon
        t_n: side length (tangent-to-tangent segment) of circumscribed regular n-gon

    Bounds:
        (n * s_n) / 2 <= pi <= (n * t_n) / 2
    """

    ### Two helper methods.
    @staticmethod
    def _validate_positive_int(n: int, name: str) -> None:
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"{name} must be a positive integer; got {n!r}")

    @staticmethod
    def _validate_n_is_power_of_two_multiple_of_six(n: int) -> None:
        """
        In this assignment we iterate: 6 -> 12 -> 24 -> ... by doubling.
        So n must be 6 * 2^k for some k >= 0.
        """
        if n % 6 != 0:
            raise ValueError(f"n must be a multiple of 6; got n={n}")
        m = n // 6
        # m must be a power of two (including 1).
        if m & (m - 1) != 0:
            raise ValueError(f"n must be 6 * 2^k; got n={n}")

    # ----------------------------
    # Recurrences from lecture 7
    # ----------------------------

    @staticmethod
    def inscribed_update(s_n: float) -> float:
        """
        Compute s_{2n} from s_n for the inscribed polygon (unit circle).

        Lecture recurrence:
            s_{2n} = sqrt( 2 - sqrt(4 - s_n^2) )

        Args:
            s_n: inscribed side length at n sides.

        Returns:
            s_2n: inscribed side length at 2n sides.
        """
        if s_n <= 0.0:
            raise ValueError(f"s_n must be > 0; got {s_n}")
        inside = 4.0 - (s_n * s_n)
        if inside <= 0.0:
            # In exact math, s_n^2 < 4 for valid chords on unit circle.
            # Numerical noise could push it to <= 0; we guard explicitly.
            raise ValueError(f"Invalid s_n leading to sqrt(4 - s_n^2) with inside={inside}")
        return sqrt(2.0 - sqrt(inside))

    @staticmethod
    def circumscribed_update(t_n: float) -> float:
        """
        Compute t_{2n} from t_n for the circumscribed polygon (unit circle).

        Lecture recurrence:
            t_{2n} = 4( sqrt(1 + t_n^2/4) - 1 ) / t_n

        Args:
            t_n: circumscribed side length at n sides.

        Returns:
            t_2n: circumscribed side length at 2n sides.
        """
        if t_n <= 0.0:
            raise ValueError(f"t_n must be > 0; got {t_n}")
        return (4.0 * (sqrt(1.0 + (t_n * t_n) / 4.0) - 1.0)) / t_n

    # ----------------------------
    # Bounds & iteration utilities
    # ----------------------------

    @staticmethod
    def pi_bounds_from_s_t(n: int, s_n: float, t_n: float) -> Tuple[float, float]:
        """
        Compute (pi_lower, pi_upper) from n, s_n, t_n on the unit circle.

        pi_lower = (n * s_n) / 2
        pi_upper = (n * t_n) / 2
        """
        archimedes_pi._validate_positive_int(n, "n")
        if s_n <= 0.0 or t_n <= 0.0:
            raise ValueError(f"s_n and t_n must be > 0; got s_n={s_n}, t_n={t_n}")
        
        pi_lower = (n * s_n) / 2.0
        pi_upper = (n * t_n) / 2.0
        return pi_lower, pi_upper


    @staticmethod
    def initial_hexagon() -> Tuple[int, float, float]:
        """
        Initialization at n=6 (unit circle):
            s_6 = 1
            t_6 = 2/sqrt(3)
        """
        n = 6
        s6 = 1.0
        t6 = 2.0 / sqrt(3.0)
        return n, s6, t6


    @staticmethod
    def archimedes_pi(n: int) -> float:
        """
        Compute an approximation of pi using Archimedes' method.
        
        Parameters
        ----------
        n : int
        Number of polygon sides (must be divisible by 6).
        
        Returns
        -------
        float
        Midpoint of the lower and upper bounds on pi.
        """
        if n < 6 or n % 6 != 0:
            raise ValueError("n must be >= 6 and divisible by 6")

        s = 1.0                 # s_6
        t = 2.0 / math.sqrt(3)  # t_6
        sides = 6

        ### Dive into this loop
        while sides < n:

            # 1) Recompute s and t according to the recurrences
            # 2) double sides
            
            s = archimedes_pi.inscribed_update(s)
            t = archimedes_pi.circumscribed_update(t)
            sides *= 2

        ### compute the final estimates.
        pi_lower = (sides * s) / 2.0
        pi_upper = (sides * t) / 2.0

        ### return the average
        return 0.5 * (pi_lower + pi_upper)


    @staticmethod
    def run_table(max_n: int = 12288) -> List[ArchimedesRow]:
        """
        Run Archimedes' method by doubling n starting from 6 until n == max_n.

        Args:
            max_n: final number of sides (must be 6 * 2^k).

        Returns:
            List of ArchimedesRow rows, including the initial n=6 row.
        """
        archimedes_pi._validate_positive_int(max_n, "max_n")
        archimedes_pi._validate_n_is_power_of_two_multiple_of_six(max_n)

        n, s_n, t_n = archimedes_pi.initial_hexagon()

        rows: List[ArchimedesRow] = []
        pi_lo, pi_hi = archimedes_pi.pi_bounds_from_s_t(n, s_n, t_n)
        rows.append(ArchimedesRow(n=n, pi_lower=pi_lo, pi_upper=pi_hi, gap=pi_hi - pi_lo))

        while n < max_n:
            s_n = archimedes_pi.inscribed_update(s_n)
            t_n = archimedes_pi.circumscribed_update(t_n)
            n *= 2

            pi_lo, pi_hi = archimedes_pi.pi_bounds_from_s_t(n, s_n, t_n)
            rows.append(ArchimedesRow(n=n, pi_lower=pi_lo, pi_upper=pi_hi, gap=pi_hi - pi_lo))

        return rows

    @staticmethod
    def print_table(max_n: int = 12288) -> None:
        """
        Print a table in the same style as the lecture sample run.

        Example:
             n        pi_lower        pi_upper             gap
        ------------------------------------------------------------
             6  3.000000000000  3.464101615138 4.641016151378e-01
             ...
        """
        rows = archimedes_pi.run_table(max_n=max_n)

        print(f"{'n':>6} {'pi_lower':>15} {'pi_upper':>15} {'gap':>16}")
        print("-" * 60)
        for r in rows:
            print(f"{r.n:6d} {r.pi_lower:15.12f} {r.pi_upper:15.12f} {r.gap:16.12e}")


if __name__ == "__main__":
    # Default demo run to mirror the lecture table.
    archimedes_pi.print_table(max_n=12288)
