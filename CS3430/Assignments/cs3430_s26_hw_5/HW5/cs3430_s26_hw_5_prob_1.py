"""
Problem One Write Up:

This problem implements continued fraction generators and pi and e using mpmath, and decimal implementations.

We computed the convergents of the continued fractions and then compared them against the actual values of pi and e 
to see how our approximations improve with each iteration, but also see at what point should we stop doing iterations
because the precision does not get significantly better.

I verified the correctness of the generators by running the unit tests which compares the approximations against the
oracle values of pi and e, and checks that the approximations match with each iteration, which they do. 

Every function is is found and callable, and fixed precision values for mpath and decimal were set to 90, and each generator 
produces approximations.

1) How quickly the convergents approach machine precision:

    In the unit test we are using mp.dps and prec = 90 for both the mpmath and decimal fraction generators. 

    For mpmath in the first few convergents matches the oracle value of e and pi with a difference of 0 this
    indicates that we can reach our machine precision in a small number of iterations.

    For decimal the first few convergents matches the oracle value of e and pi, but with a bigger difference of 0E-89 
    up to 1E-89. This indicates that we can reach our machine precision in a small number of iterations, with a 
    difference thats slightly bigger than mpmath, but still very small, and most likely due to the fact that decimal
    is base 10, thus it will round differently than mpmath which is base 2.


2) Do mpMath and decimal behave differently?

    Yes, both behave differently, however I think its important to note that does not make either of them incorrect. 

    mpmath uses binary floating point precision, which is controlled by mp.dps
    decimal uses base-10 floating point precision which is controlled by the context precision.

    with both set to 90 in this case, the differences are different because of how each one
    handles precision and rounding

3) How many iterations are needed before further progress becomes meaningless?

    Once we hit our 90 digits of precision, additional convergents may improve the mathematical convergence,
    but we will hit our visible representation limits.  further convergents won't privide any meaningful
    improvement.

"""
# cs3430_s26_hw_5_prob_1.py
#
# CS3430 S26: Scientific Computing (HW 5, Problem 1)
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
# Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
#
# -----------------------------------------------------------------------------
# Problem 1 Theme (Lecture 8 / Transcendental Meditation):
#   - Continued fractions are infinite objects; we approximate them via convergents.
#   - Generators encode *processes* (rules for producing the next value), not containers.
#     There is no universal prev(generator). Once a generator advances, it does not go back.
#   - Representation matters:
#       * mpmath uses arbitrary-precision binary floating-point (mp.mpf) controlled by mp.dps.
#       * decimal uses arbitrary-precision base-10 floating-point (Decimal) controlled by context precision.
#   - IMPORTANT EXPECTATION:
#       We are NOT trying to “beat” mpmath with decimal or vice versa.
#       We are observing when further iterations stop improving agreement with a fixed benchmark.
#       (e.g., math.pi / math.e or numpy equivalents) due to representation limits.
#
#  You know the drill: Read the code and replace # YOUR CODE HERE with your code blocks.
# -----------------------------------------------------------------------------

from __future__ import annotations

# -----------------------------------------------------------------------------
# Why these imports are here
# -----------------------------------------------------------------------------

# dataclass is a standard-library decorator for defining small, structured
# data objects. In scientific computing, we often want to bundle related
# values together (e.g., precision, iteration count, error) in a clear,
# named way instead of using anonymous tuples like (a, b, c).
#
# Even if this homework does not strictly require a dataclass immediately,
# I include it to model good professional practice that you can follow in
# the future to make your code easier to extend without redesign.
from dataclasses import dataclass

# Decimal provides arbitrary-precision base-10 floating-point arithmetic.
# This is fundamentally different from Python's built-in float, which uses
# fixed-precision binary arithmetic.
#
# In this homework, we will use Decimal to explore how representation choice
# affects numerical convergence and visible accuracy.
#
# localcontext() allows us to set decimal precision locally and temporarily.
# This avoids global side effects and ensures that each computation is carried
# out under a clearly defined precision setting.
#
# In scientific computing, precision is part of the algorithm/method design, not an
# accidental global setting.
from decimal import Decimal, localcontext
from typing import Generator, Iterable, Iterator, List, Optional, Sequence, Tuple, Union

from mpmath import mp

# NOTE ON THE * NOTATION IN SOME FUNCTION SIGNATURES BELOW.
# E.g.,
#
#     pi_cf_dec(*, prec: int = 50) -> Iterator[Decimal]
#
# The lone '*' means that 'prec' is a keyword-only argument.
#
# This forces calls to look like:
#     pi_cf_dec(prec=80)
#
# and prevents ambiguous or accidental calls like:
#     pi_cf_dec(80)
#
# In scientific computing, explicitness matters:
#   - precision is part of the experiment,
#   - making it keyword-only reduces mistakes and improves readability.

# ----------------------------- Helpers -----------------------------

def _eval_cf_mp(Ns: Sequence[mp.mpf], Ds: Sequence[mp.mpf]) -> mp.mpf:
    """
    Evaluate a finite continued fraction (a convergent) inside-out using mpmath types.

    Given equal-length sequences Ns and Ds (both 1-indexed conceptually),
    compute:

        x_k = N_k / D_k
        x_j = N_j / (D_j + x_{j+1})   for j=k-1,...,1

    Returns the value x_1.

    Notes:
      - Inside-out evaluation is essential: the fraction is nested.
      - We recompute the convergent each iteration from stored coefficients.
        This is deliberate and matches the lecture's emphasis (no backward generator travel).
    """
    if len(Ns) != len(Ds):
        raise ValueError("Ns and Ds must have the same length.")
    if not Ns:
        raise ValueError("Ns and Ds must be non-empty.")

    # We start with the innermost fraction:
    #
    #     x_k = N_k / D_k
    #
    
    x = Ns[-1] / Ds[-1]
    
    # And, then we "wrap outward" to compute:
    #
    #     x_{k-1} = N_{k-1} / (D_{k-1} + x_k)
    #     x_{k-2} = N_{k-2} / (D_{k-2} + x_{k-1})
    #     ...
    #     x_1
    #
    # This is why continued fractions must be evaluated inside-out.
    # There is no valid outside-in evaluation order for nested fractions.
    #
    # You can use reversed(Ns[:-1]) to produce the sequence:
    #     N_{k-1}, N_{k-2}, ..., N_1
    #
    # You can use reversed(Ds[:-1]) to produce the sequence:
    #     D_{k-1}, D_{k-2}, ..., D_1
    #
    # You can use zip(...) on the two reversed pairs above; these values group position-by-position so that each N_j
    # is matched with its corresponding D_j as we move outward.
    #
    # This exactly mirrors the mathematical recurrence discussed in lecture:
    #
    #     x_j = N_j / (D_j + x_{j+1})
    #
    # NB:
    #   - We cannot "go backward" in a generator.
    #   - Therefore, when a new (N_i, D_i) pair is added, we must recompute
    #     the convergent from the inside out using the coefficients seen so far.

    # Wrap outward (inside-out)
    # This loop is the computational translation of that mathematical rule that
    # the generator will use.

    # YOUR CODE HERE. One for-loop over a zip of two reverseds will suffice.
    for N_j, D_j in zip(reversed(Ns[:-1]), reversed(Ds[:-1])):
        x = N_j / (D_j + x)
        
    return x


def _eval_cf_dec(Ns: Sequence[Decimal], Ds: Sequence[Decimal], *, prec: int) -> Decimal:
    """
    Evaluate a finite continued fraction (a convergent) inside-out using Decimal.

    We evaluate inside a local decimal context with precision `prec` so that:
      - all intermediate results are rounded consistently,
      - the generator's behavior is repeatable and controlled.

    NB:
      - decimal precision is *finite*. Past a point, additional iterations will not improve
        the printed digits, even if the mathematics continues to converge.
    """
    if len(Ns) != len(Ds):
        raise ValueError("Ns and Ds must have the same length.")
    if not Ns:
        raise ValueError("Ns and Ds must be non-empty.")

    # This mirrors the upper helper. We evaluate the continued fraction below inside a local decimal context.
    #
    # localcontext() creates a temporary decimal environment in which we can:
    #   - set a specific precision,
    #   - perform computations,
    #   - and then automatically restore the previous global context.
    #
    # This is critical in scientific computing:
    #   - precision is part of the experiment,
    #   - we do NOT want one computation to silently affect another.
    #
    # By setting ctx.prec = prec, we explicitly control how many significant
    # decimal digits are retained during ALL intermediate operations.
    #
    # This mirrors the lecture point that:
    #   representation limits are real, observable, and deliberate.    
    with localcontext() as ctx:
        ctx.prec = prec
        # As with the mpmath version, we start from the innermost fraction:
        #
        #     x_k = N_k / D_k
        #
        # and then "wrap outward" using the recurrence:
        #
        #     x_j = N_j / (D_j + x_{j+1})
        #
        # The evaluation order is inside-out because the fraction is nested.        
        x = Ns[-1] / Ds[-1]

        # reversed(...) and zip(...) are used exactly as in the mpmath version:
        # they pair (N_{k-1}, D_{k-1}), (N_{k-2}, D_{k-2}), ..., (N_1, D_1)
        # so we can wrap outward one layer at a time.

        # YOUR CODE HERE: One for-loop over a zip of two reversed will suffice.
        for N_j, D_j in zip(reversed(Ns[:-1]), reversed(Ds[:-1])):
            x = N_j / (D_j + x)

        # The unary plus (+x) below forces Decimal to apply the current context's
        # rounding rules to the result.
        #
        # Without this, x may carry extra internal precision from intermediate
        # computations. Applying unary plus makes the rounding explicit and
        # visible, which is exactly what we want for a controlled experiment.
        #
        # This is another concrete example of the lecture theme:
        #   precision is not magic: it must be enforced deliberately.            
        return +x  # unary plus applies the current context rounding

# ------------------------- Continued-fraction generators -------------------------

def pi_cf_mp(*, dps: int = 50) -> Iterator[mp.mpf]:
    """
    Yield successive convergents for pi using the generalized continued fraction from Lecture 8:

        pi = 3 + x
        x = 1^2 / (6 + 3^2 / (6 + 5^2 / (6 + 7^2 / (6 + ...))))

    Coefficients:
        N_i = (2i - 1)^2
        D_i = 6

    Each yield returns an mp.mpf approximation to pi.

    Parameters
    ----------
    dps (decimal places):
        mpmath working decimal precision. This controls accuracy, not just printing.
        Setting dps too low may cause convergence to "stop early" due to representation limits.
    """
    # 1) We set the working decimal precision for mpmath.
    #
    # mp.dps controls how many *decimal digits* of precision mpmath uses
    # internally. This affects all mp.mpf computations that follow.
    #
    # IMPORTANT:
    #   - mp.dps controls accuracy, not just printing.
    #   - If mp.dps is too small, convergence may appear to "stop early"
    #     even though the mathematics continues to converge.
    
    # YOUR CODE HERE.
    mp.dps = dps


    # Ns and Ds store the continued-fraction coefficients accumulated so far.
    #
    # These lists grow monotonically as the generator advances.
    # We intentionally keep them because:
    #   - generators cannot go backward,
    #   - each new convergent depends on *all* previous coefficients.
    #
    # Recomputing the convergent from these stored coefficients mirrors the
    # inside-out evaluation rule discussed in lecture.    
    Ns: List[mp.mpf] = []
    Ds: List[mp.mpf] = []

    # Index i corresponds to the continued-fraction level (i = 1, 2, 3, ...).
    i = 1

    # 2) Pre-define constants as mp.mpf values to avoid accidental mixing
    # of Python ints/floats with mpmath numbers. These are the numbers
    # we use in our continued fraction approximation.
    six = mp.mpf("6")
    three = mp.mpf("3")

    # Our generator is intentionally infinite.
    #
    # Continued fractions are infinite objects by definition.
    # We control approximation quality by how many values we consume,
    # not by terminating the generator.    
    while True:
        # 1) For the pi continued fraction from Lecture 8:
        #
        #     N_i = (2i - 1)^2
        #     D_i = 6
        #
        # Each iteration adds one more layer to the fraction.
        # 1.a) compute N_i and append it to Ns.

        # YOUR CODE HERE
        N_i = (2 * i - 1) ** 2
        Ns.append(mp.mpf(N_i))

        # 1.b) Compute D_i and append it to Ds. Use six above.
        # YOUR CODE HERE
        Ds.append(six)

        # 2) Evaluate the current convergent using inside-out evaluation.
        # with _eval_cf_mp helper.
        # This recomputes the value from all coefficients seen so far.
        # This is not wasteful; it is the correct computational translation
        # of the mathematics and respects the forward-only nature of generators.
        # Save your result in the local variable x

        # YOUR CODE HERE
        x = _eval_cf_mp(Ns, Ds)
        
        # 3) Add back the integer part:
        #
        #     pi = 3 + x
        #
        # and yield (no return!) the current approximation.
        # Use three and x here.

        # YOUR CODE HERE.
        yield three + x

        # 4) Advance to the next level of the continued fraction.
        i += 1


def _e_D_i(i: int) -> int:
    """
    Return D_i for the continued fraction of (e - 2) used in Lecture 8:

        D_i = 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, ...

    Pattern:
        D_1 = 1
        For i >= 2:
          - if i % 3 == 2 then D_i = 2 * ((i + 1) // 3)
          - otherwise D_i = 1
    """
    # YOUR CODE HERE.
    if i % 3 == 2:
        return 2 * ((i + 1) // 3)
    else:
        return 1


def e_cf_mp(*, dps: int = 50) -> Iterator[mp.mpf]:
    """
    Yield successive convergents for e using the Lecture 8 continued fraction:

        e = 2 + x
        x = 1 / (1 + 1 / (2 + 1 / (1 + 1 / (1 + 1 / (4 + ...)))))

    Coefficients:
        N_i = 1
        D_i = 1, 2, 1, 1, 4, 1, 1, 6, ...

    Each yield returns an mp.mpf approximation to e.
    """
    # 1) We set the working decimal precision for mpmath.
    #
    # As in the pi generator, mp.dps controls the actual numerical precision
    # of all mp.mpf computations that follow, not just how many digits are printed.
    #
    # If mp.dps is too small, convergence may appear to stall even though the
    # continued fraction is still converging mathematically.

    # YOUR CODE HERE.
    mp.dps = dps

    # Ns and Ds store the accumulated continued-fraction coefficients for (e - 2).
    #
    # For this continued fraction:
    #   - all numerators are N_i = 1
    #   - denominators follow a repeating pattern (defined by _e_D_i)
    #
    # As with pi, we must retain all coefficients seen so far because:
    #   - generators cannot move backward,
    #   - each new convergent depends on *all* previous layers.
    Ns: List[mp.mpf] = []
    Ds: List[mp.mpf] = []

    # Index i tracks the depth of the continued fraction (i = 1, 2, 3, ...).
    i = 1

    # Define constants explicitly as mp.mpf values to avoid mixing Python
    # integers with mpmath numbers.    
    one = mp.mpf("1")
    two = mp.mpf("2")

    # This generator is intentionally infinite.
    #
    # Continued fractions are infinite objects by definition.
    # We control approximation quality by how many values we *consume*,
    # not by terminating the generator.
    #
    # This matches the lecture principle that approximation is controlled
    # externally (by truncation), not internally (by stopping rules).
    while True:
        # 1) For the continued fraction of (e - 2):
        #
        #     N_i = 1
        #     D_i = 1, 2, 1, 1, 4, 1, 1, 6, ...
        #
        # The denominator pattern is encoded in the helper function _e_D_i(i).
        Ns.append(one)
        Ds.append(mp.mpf(_e_D_i(i)))

        # 2) Evaluate the current convergent using inside-out evaluation.
        # Use the _eval_cf_mp helper.
        # As discussed in lecture, there is no valid outside-in evaluation
        # order for nested continued fractions. Save the result in variable x.

        # YOUR CODE HERE.
        x = _eval_cf_mp(Ns, Ds)

        # 3) Add back the integer part:
        #
        #     e = 2 + x
        #
        # and yield the current approximation, i.e., two + x.

        # YOUR CODE HERE.
        yield two + x
        
        # 4) Advance to the next continued-fraction level.
        i += 1

def pi_cf_dec(*, prec: int = 50) -> Iterator[Decimal]:
    """
    Yield successive convergents for pi (Lecture 8 continued fraction) using Decimal arithmetic.

    NB:
      - Decimal arithmetic is base-10 with finite precision set by `prec`.
      - This generator evaluates each convergent inside a local context of precision `prec`.

    Parameters
    ----------
    prec:
        Decimal working precision (number of significant digits). Controls accuracy.
    """
    # Ns and Ds store the accumulated continued-fraction coefficients.
    #
    # As in the mpmath version, these lists grow monotonically and store
    # all coefficients seen so far.
    #
    # This is necessary because:
    #   - generators cannot move backward,
    #   - each new convergent depends on all previous layers of the fraction.
    Ns: List[Decimal] = []
    Ds: List[Decimal] = []

    # Index i tracks the depth of the continued fraction (i = 1, 2, 3, ...).
    i = 1

    # Define constants explicitly as Decimal values.
    #
    # Using strings avoids accidentally introducing binary floating-point
    # rounding before Decimal ever sees the number.
    six = Decimal("6")
    three = Decimal("3")

    # This generator is intentionally infinite.
    #
    # Continued fractions are infinite objects by definition.
    # Approximation quality is controlled by how many values are *consumed*
    # and by the Decimal precision, not by terminating the generator.    
    while True:
        # 1) For the pi continued fraction from Lecture 8:
        #
        #     N_i = (2i - 1)^2
        #     D_i = 6
        #
        # Each iteration adds one more layer to the continued fraction.
        odd = 2 * i - 1
        Ns.append(Decimal(odd * odd))
        Ds.append(six)

        # 2) Evaluate the current convergent using Decimal arithmetic.
        # Use _eval_cf_dec helper here.
        # The evaluation is performed inside a local decimal context
        # (i.e., in _eval_cf_dec), where the precision 'prec' is enforced.
        #
        # This makes representation limits visible: at some point,
        # additional iterations will stop improving the result.
        # Save the result in variable x.

        # YOUR CODE HERE
        x = _eval_cf_dec(Ns, Ds, prec=prec)

        # 3) Add back the integer part:
        #
        #     pi = 3 + x
        #
        # and yield the current Decimal approximation as three + x.
        
        # YOUR CODE HERE
        yield three + x

        # 4) Advance to the next level of the continued fraction.
        i += 1


def e_cf_dec(*, prec: int = 50) -> Iterator[Decimal]:
    """
    Yield successive convergents for e (Lecture 8 continued fraction) using Decimal arithmetic.

    Parameters
    ----------
    prec:
        Decimal working precision (number of significant digits). Controls accuracy.
    """
    Ns: List[Decimal] = []
    Ds: List[Decimal] = []
    i = 1
    one = Decimal("1")
    two = Decimal("2")

    # Nothing complicated here.
    while True:
        Ns.append(one)
        Ds.append(Decimal(_e_D_i(i)))

        x = _eval_cf_dec(Ns, Ds, prec=prec)
        yield two + x
        i += 1
