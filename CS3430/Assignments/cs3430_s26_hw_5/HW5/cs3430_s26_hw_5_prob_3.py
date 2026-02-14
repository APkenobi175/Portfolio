# cs3430_s26_hw_5_prob_3.py
#
# CS3430 S26: Scientific Computing (HW 5, Problem 3)
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
# Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Tuple

from mpmath import mp

def pi_ramanujan_mp(*, dps: int = 50) -> Iterator[mp.mpf]:
    """
    Generator for successive approximations of pi using a Ramanujan-type series.

    Ramanujan (1914) gave a famous series for 1/pi:

        1/pi = (2*sqrt(2) / 9801) * sum_{k=0}^∞
               ( (4k)! * (1103 + 26390 k) ) / ( (k!)^4 * 396^(4k) )

    Key scientific-computing lesson:
      - This converges *extremely* fast (a few terms can exceed float precision).
      - With mpmath, we can choose working precision (mp.dps) and actually observe it.

    This generator yields pi approximations directly, one per added term in the sum:
      - after k=0 term, yield pi_0
      - after k=0..1 terms, yield pi_1
      - etc.

    Notes:
      - We use mp.factorial for clarity. For small k (as in this homework), that's fine.
      - The heavy point is not micro-optimization; it's convergence vs representation.
    """
    # 1) Set the precision.
    mp.dps = dps

    # 2) Constant multiplier in Ramanujan's formula for 1/pi.
    const = (mp.mpf("2") * mp.sqrt(mp.mpf("2"))) / mp.mpf("9801")

    # 3) Running sum for the series (in high precision).
    s = mp.mpf("0")

    k = 0
    while True:
        # 1) compute term_k = (4k)! * (1103 + 26390k) / ((k!)^4 * 396^(4k))
        # you can use mp.factorial(4*k) * (mp.mpf("1103") + mp.mpf("26390") * k) in the numerator
        # and (mp.factorial(k) ** 4) * (mp.mpf("396") ** (4 * k)) in the denominator. then
        # term = num / den

        # YOUR CODE HERE
        
        # 1a. Compute the numerator
        num = mp.factorial(4 * k) * (mp.mpf("1103") + mp.mpf("26390") * k)
        # 1b. Compute the denominator
        den = (mp.factorial(k) ** 4) * (mp.mpf("396") ** (4 * k))
        # 1c. Compute the term
        term = num / den

        # 2) Add the term to the sum
        s += term

        # 3) Now 1/pi ≈ const * s  =>  pi ≈ 1 / (const*s)
        inv_pi = const * s
        pi_approx = mp.mpf("1") / inv_pi

        # 4) Yield
        yield pi_approx

        # 5) Advance
        k += 1


# ------------------------- Chudnovsky via Binary Splitting -------------------------

@dataclass(frozen=True)
class _BSTuple:
    """
    Container for the binary splitting triple (P, Q, T), all as Python integers.

    We compute these as *exact integers* and only convert to mp.mpf at the end.
    This is the entire point of binary splitting: keep intermediate arithmetic exact.
    """
    P: int
    Q: int
    T: int


def _chudnovsky_bs(a: int, b: int, C3_OVER_24: int) -> _BSTuple:
    """
    Binary splitting for the Chudnovsky series from term indices [a, b).

    We build integers P(a,b), Q(a,b), T(a,b) such that:

      sum_{k=a}^{b-1} (-1)^k * (6k)! * (13591409 + 545140134k)
      ---------------------------------------------------------
                 (3k)! (k!)^3 * 640320^(3k)

    can be represented as T / Q (up to a scaling convention).
    Binary splitting reduces repeated big-integer work.

    Combine rule (standard binary split identity):

      (P1, Q1, T1) for [a,m)
      (P2, Q2, T2) for [m,b)

      P = P1 * P2
      Q = Q1 * Q2
      T = T2 * P1 + T1 * Q2

    Base case (single k):
      Pk = (6k-5)(2k-1)(6k-1)   for k >= 1, and P0 = 1
      Qk = k^3 * C3_OVER_24     for k >= 1, and Q0 = 1
      Tk = Pk * (13591409 + 545140134k) with alternating sign
           and with T0 = 13591409

    This is a well-known exact integer formulation used in record pi computations.
    """
    if b - a == 1:
        k = a
        if k == 0:
            # k=0 term special-cases nicely.
            return _BSTuple(P=1, Q=1, T=13591409)

        # Compute Pk, Qk as exact ints.
        Pk = (6 * k - 5) * (2 * k - 1) * (6 * k - 1)
        Qk = (k * k * k) * C3_OVER_24

        # Linear factor in numerator.
        Ak = 13591409 + 545140134 * k

        Tk = Pk * Ak
        if k % 2 == 1:
            Tk = -Tk

        return _BSTuple(P=Pk, Q=Qk, T=Tk)

    m = (a + b) // 2
    left = _chudnovsky_bs(a, m, C3_OVER_24)
    right = _chudnovsky_bs(m, b, C3_OVER_24)

    P = left.P * right.P
    Q = left.Q * right.Q
    T = right.T * left.P + left.T * right.Q

    return _BSTuple(P=P, Q=Q, T=T)


def _pi_from_chudnovsky_bs(n_terms: int) -> mp.mpf:
    """
    Compute pi using n_terms of Chudnovsky series via binary splitting.

    The classic Chudnovsky formula:

      1/pi = (1 / (426880*sqrt(10005))) * sum_{k=0}^∞
             (-1)^k (6k)! (13591409 + 545140134k)
             -------------------------------------
             (3k)! (k!)^3 640320^(3k)

    Binary splitting produces an exact rational T/Q (up to scaling),
    and then we multiply by 426880*sqrt(10005) to recover pi.

    This function intentionally separates:
      - exact big-integer work (P,Q,T),
      - high-precision conversion (mp.mpf),
      - final sqrt scaling (mp.sqrt).
    """
    if n_terms <= 0:
        raise ValueError("n_terms must be positive")

    # Constants in the Chudnovsky formulation.
    C = 640320
    C3_OVER_24 = (C ** 3) // 24  # exact int

    # Binary split across k = 0..n_terms-1
    bs = _chudnovsky_bs(0, n_terms, C3_OVER_24)

    # Convert exact ints to mp.mpf at the end.
    Q = mp.mpf(bs.Q)
    T = mp.mpf(bs.T)

    # Multiply by the scaling constant:
    # pi = (Q * 426880 * sqrt(10005)) / T
    K = mp.mpf("426880") * mp.sqrt(mp.mpf("10005"))
    return (Q * K) / T


def pi_chudnovsky_bs_mp(*, dps: int = 50) -> Iterator[mp.mpf]:
    """
    Generator for successive approximations of pi using the Chudnovsky series
    with a binary splitting backend.

    Each yielded value corresponds to increasing the number of series terms:
      - yield pi computed with 1 term (k=0)
      - yield pi computed with 2 terms (k=0..1)
      - etc.

    Key takeaway:
      - Convergence is so fast that with insufficient mp.dps,
        additional terms appear to 'stop helping' (representation bottleneck).
      - Binary splitting makes large-term computations feasible by using exact ints.
    """
    mp.dps = dps

    n = 1
    while True:
        
        # 1) yield a call to _pi_from_chudnovsky(n_terms=n)

        # YOUR CODE HERE
        yield _pi_from_chudnovsky_bs(n_terms=n)

        # 2) Move forward.
        n += 1
