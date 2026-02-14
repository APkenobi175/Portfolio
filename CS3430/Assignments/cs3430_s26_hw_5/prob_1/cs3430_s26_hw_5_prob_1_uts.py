# cs3430_s26_hw_5_prob_1_uts.py
#
# CS3430 S26: Scientific Computing (HW 5, Problem 1 UTs)
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
# Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
#
# Unit tests for CS3430 S26: Scientific Computing (HW 5, Problem 1)
#
# These unit tests intentionally split:
#   (1) structural checks and (2) numerical correctness checks
# as per course conventions.
#
# Success print statements use "!!!" for Ubuntu terminal compatibility.

from __future__ import annotations

import unittest
from decimal import Decimal, localcontext

# Fraction provides exact rational arithmetic using arbitrary-size integers.
#
# Unlike float, Decimal, or mpmath, Fraction performs no rounding at all:
# every value is represented exactly as a ratio of two integers.
#
# In our unit tests, Fraction is used to build a ground-truth oracle:
#   - continued fractions with integer coefficients always evaluate to
#     exact rational numbers at any finite truncation,
#   - Fraction lets us compute those exact values with zero numerical error.
#
# We do NOT use Fraction in the problem source code because:
#   - it does not model real numerical computation,
#   - it hides convergence and representation limits,
#   - it would defeat the purpose of the experiment.
#
# In short:
#   - Fraction is great for verification (tests),
#   - mpmath and Decimal are for approximation (SciComp solutions).

from fractions import Fraction
from typing import Iterable, Iterator, List, Sequence, Tuple

from mpmath import mp

import cs3430_s26_hw_5_prob_1 as prob1

# ------------------------------ Oracles ------------------------------

def _eval_cf_fraction(Ns: Sequence[int], Ds: Sequence[int]) -> Fraction:
    # This function evaluates a finite continued fraction *exactly*
    # using Fraction arithmetic.
    #
    # It serves as a *test oracle*, not as a numerical method.
    #
    # Because all N_i and D_i values are integers, every finite truncation
    # of a continued fraction is a rational number. Fraction represents
    # these rationals exactly as numerator/denominator pairs with no
    # rounding and no loss of information.
    #
    # This allows us to compare student implementations (mpmath / Decimal)
    # against a mathematically exact reference.

    # Sanity check for oracle inputs:
    #   - Ns and Ds must have the same length,
    #   - the sequences must not be empty.
    #
    # If this fails, the test setup itself is wrong.
    if len(Ns) != len(Ds) or not Ns:
        raise ValueError("Bad oracle inputs.")

    # Start with the innermost fraction:
    #
    #     x_k = N_k / D_k
    #
    # This value is exact because Fraction performs rational arithmetic.
    x = Fraction(Ns[-1], Ds[-1])

    # Wrap outward using inside-out evaluation:
    #
    #     x_j = N_j / (D_j + x_{j+1})
    #
    # reversed(...) produces:
    #     N_{k-1}, N_{k-2}, ..., N_1
    #     D_{k-1}, D_{k-2}, ..., D_1
    #
    # zip(...) pairs the corresponding numerator and denominator at each
    # level so that the recurrence is applied correctly.
    for N, D in zip(reversed(Ns[:-1]), reversed(Ds[:-1])):
        x = Fraction(N, D + x)

    # Return the exact rational value of the convergent.
    #
    # This value is used as ground truth when validating approximate
    # computations performed with mpmath and Decimal.
    return x

def _pi_convergents_exact(k: int) -> List[Fraction]:
    # This function generates the first k *exact* convergents of pi
    # using Fraction arithmetic.
    #
    # IMPORTANT:
    #   - This is a test oracle, not a numerical algorithm.
    #   - It computes the mathematically exact rational values of the
    #     truncated continued fraction for pi.
    #
    # Each convergent has the form:
    #
    #     pi_k = 3 + x_k
    #
    # where x_k is the k-level truncation of the continued fraction
    # discussed in Lecture 8.

    # Ns and Ds store the integer coefficients of the continued fraction
    # accumulated so far.
    #
    # These are plain Python integers, which is sufficient because
    # Fraction will handle arbitrary-size integer arithmetic exactly.
    Ns: List[int] = []
    Ds: List[int] = []

    # out will store the exact rational convergents of pi.
    out: List[Fraction] = []

    # Build convergents incrementally, one level at a time.
    #
    # The loop index i corresponds to the continued-fraction depth.
    for i in range(1, k + 1):
        # For the pi continued fraction from Lecture 8:
        #
        #     N_i = (2i - 1)^2
        #     D_i = 6
        #
        # These coefficients are integers, so the resulting convergent
        # is an exact rational number.
        odd = 2 * i - 1
        Ns.append(odd * odd)
        Ds.append(6)

        # Evaluate the current convergent exactly using Fraction arithmetic.
        #
        # _eval_cf_fraction performs inside-out evaluation with no rounding.
        # We then add back the integer part:
        #
        #     pi = 3 + x_k
        #
        # to obtain the full pi approximation at depth i.
        out.append(Fraction(3, 1) + _eval_cf_fraction(Ns, Ds))

    # Return the list of exact rational convergents.
    #
    # These values serve as ground truth for validating approximate
    # computations performed with mpmath and Decimal.
    return out


def _e_D_i(i: int) -> int:
    """Same D_i pattern replicated for oracle generation."""
    if i == 1:
        return 1
    if i % 3 == 2:
        return 2 * ((i + 1) // 3)
    return 1

def _e_convergents_exact(k: int) -> List[Fraction]:
    # This function generates the first k *exact* convergents of e
    # using Fraction arithmetic.
    #
    # As with the pi oracle, this function is used only in unit tests
    # to provide mathematically exact reference values.
    #
    # Each convergent has the form:
    #
    #     e_k = 2 + x_k
    #
    # where x_k is the k-level truncation of the continued fraction
    # for (e - 2) discussed in Lecture 8.

    # Ns and Ds store the integer coefficients of the continued fraction
    # accumulated so far.
    #
    # For e:
    #   - all numerators are N_i = 1
    #   - denominators follow a structured, non-constant pattern
    #     encoded by the helper function _e_D_i(i).
    Ns: List[int] = []
    Ds: List[int] = []

    # out will store the exact rational convergents of e.
    out: List[Fraction] = []

    # Build convergents incrementally, one level at a time.
    #
    # The loop index i corresponds to the depth of the continued fraction.
    for i in range(1, k + 1):
        # Append the next continued-fraction coefficients.
        #
        # N_i = 1 for all i
        # D_i is determined by the repeating pattern in _e_D_i(i).
        Ns.append(1)
        Ds.append(_e_D_i(i))

        # Evaluate the current convergent exactly using Fraction arithmetic.
        #
        # _eval_cf_fraction performs inside-out evaluation with no rounding.
        # We then add back the integer part:
        #
        #     e = 2 + x_k
        #
        # to obtain the full approximation at depth i.
        out.append(Fraction(2, 1) + _eval_cf_fraction(Ns, Ds))

    # Return the list of exact rational convergents.
    #
    # These values serve as ground truth for validating approximate
    # computations performed with mpmath and Decimal.
    return out

def _take(gen: Iterator, n: int):
    """Take n values from an iterator/generator."""
    return [next(gen) for _ in range(n)]

# --------------------------------- Tests ------------------------------------

class TestStructure(unittest.TestCase):
    # This test class checks structural properties of the student solution.
    #
    # Structural tests answer questions like:
    #   - Do the required functions exist?
    #   - Are they callable?
    #   - Do they behave like generators?
    #
    # These tests do NOT check numerical correctness.
    # They ensure the computational scaffolding is in place.

    def test_required_callables_exist(self):
        # This test verifies that the required generator functions
        # are present in the solution module and are callable.
        #
        # If any of these fail, it means the student has not implemented
        # the required interface for Problem 1.

        print("\n[STRUCTURE TEST] Checking that required generator functions exist:")

        self.assertTrue(callable(getattr(prob1, "pi_cf_mp", None)))
        print("  - pi_cf_mp: FOUND and callable")

        self.assertTrue(callable(getattr(prob1, "e_cf_mp", None)))
        print("  - e_cf_mp:  FOUND and callable")

        self.assertTrue(callable(getattr(prob1, "pi_cf_dec", None)))
        print("  - pi_cf_dec: FOUND and callable")

        self.assertTrue(callable(getattr(prob1, "e_cf_dec", None)))
        print("  - e_cf_dec:  FOUND and callable")

        print("  -> All required generator functions are present.\n")

    def test_generators_yield_multiple_values(self):
        # This test verifies that each generator:
        #   - can be instantiated,
        #   - yields multiple values,
        #   - yields values of the correct numerical type.
        #
        # This confirms that the functions are *true generators*
        # and not one-shot computations.

        print("[STRUCTURE TEST] Creating generators with fixed precision:")
        print("  - mpmath precision: dps = 80")
        print("  - decimal precision: prec = 80\n")

        g1 = prob1.pi_cf_mp(dps=80)
        g2 = prob1.e_cf_mp(dps=80)
        g3 = prob1.pi_cf_dec(prec=80)
        g4 = prob1.e_cf_dec(prec=80)

        print("  Generators created successfully.")

        # Consume the first three values from each generator.
        #
        # This advances the generator state and confirms that:
        #   - the generator does not terminate immediately,
        #   - successive approximations are produced.
        xs1 = _take(g1, 3)
        xs2 = _take(g2, 3)
        xs3 = _take(g3, 3)
        xs4 = _take(g4, 3)

        print("\n  First three approximations produced:")
        print("    pi_cf_mp:", xs1)
        print("    e_cf_mp: ", xs2)
        print("    pi_cf_dec:", xs3)
        print("    e_cf_dec: ", xs4)

        # Check that exactly three values were produced by each generator.
        self.assertEqual(len(xs1), 3)
        self.assertEqual(len(xs2), 3)
        self.assertEqual(len(xs3), 3)
        self.assertEqual(len(xs4), 3)

        print("\n  All generators yielded the expected number of values (3).")

        # Type checks:
        #
        # These ensure that:
        #   - mpmath-based generators return mp.mpf values,
        #   - decimal-based generators return Decimal values.
        #
        # Mixing types would indicate a representation error.
        self.assertTrue(all(isinstance(x, mp.mpf) for x in xs1))
        self.assertTrue(all(isinstance(x, mp.mpf) for x in xs2))
        self.assertTrue(all(isinstance(x, Decimal) for x in xs3))
        self.assertTrue(all(isinstance(x, Decimal) for x in xs4))

        print("  Type checks passed:")
        print("    - mpmath generators returned mp.mpf values")
        print("    - decimal generators returned Decimal values")
        print("\n  -> Generator structure and types are correct.\n")

class TestNumericalCorrectness(unittest.TestCase):
    # This test class checks numerical correctness by comparing
    # generated approximations against exact rational values.
    #
    # The exact values are produced by oracle functions using Fraction,
    # which performs exact arithmetic with no rounding.
    #
    # Our goal is to verify that:
    #   - each convergent is computed correctly,
    #   - mpmath and Decimal implementations match the exact mathematics
    #     up to very tight numerical tolerances.

    def test_pi_convergents_match_oracle(self):
        # Number of convergents to test.
        #
        # We do not need many here: if the first few are correct,
        # the recurrence and generator logic are almost certainly correct.
        k = 6

        print("\n[NUMERICAL TEST] Validating pi convergents against exact oracle")
        print(f"  Testing first {k} convergents\n")

        # Compute exact rational convergents using Fraction arithmetic.
        expected = _pi_convergents_exact(k)
        
        # ---------------- mpmath comparison ----------------
        #
        # We use a very high working precision so that any mismatch
        # is due to logic errors, not rounding.
        mp.dps = 90
        print("  mpmath test:")
        print("    - working precision set to mp.dps = 90")

        g_mp = prob1.pi_cf_mp(dps=90)
        got_mp = _take(g_mp, k)

        for j, (got, exp) in enumerate(zip(got_mp, expected), start=1):
            # Convert the exact Fraction value into an mp.mpf
            # so we can compare like with like.
            exp_mpf = mp.mpf(exp.numerator) / mp.mpf(exp.denominator)

            diff = mp.fabs(got - exp_mpf)
            print(f"    convergent {j}:")
            print(f"      approx = {got}")
            print(f"      exact  = {exp_mpf}")
            print(f"      |diff| = {diff}")

            self.assertTrue(
                diff < mp.mpf("1e-70"),
                f"pi_cf_mp mismatch at j={j}"
            )

        print("  -> mpmath pi convergents match exact oracle\n")

        # ---------------- decimal comparison ----------------
        #
        # As with mpmath, we enforce a high decimal precision so that
        # rounding does not mask implementation errors.
        print("  decimal test:")
        with localcontext() as ctx:
            ctx.prec = 90
            print("    - decimal context precision set to 90")

            g_dec = prob1.pi_cf_dec(prec=90)
            got_dec = _take(g_dec, k)

            for j, (got, exp) in enumerate(zip(got_dec, expected), start=1):
                exp_dec = Decimal(exp.numerator) / Decimal(exp.denominator)
                diff = abs(got - exp_dec)

                print(f"    convergent {j}:")
                print(f"      approx = {got}")
                print(f"      exact  = {exp_dec}")
                print(f"      |diff| = {diff}")

                self.assertTrue(
                    diff < Decimal("1e-70"),
                    f"pi_cf_dec mismatch at j={j}"
                )

        print("  -> decimal pi convergents match exact oracle\n")

    def test_e_convergents_match_oracle(self):
        # Number of convergents to test for e.
        #
        # We test slightly more than for pi because the denominator
        # pattern is more complex.
        k = 8

        print("\n[NUMERICAL TEST] Validating e convergents against exact oracle")
        print(f"  Testing first {k} convergents\n")

        # Compute exact rational convergents using Fraction arithmetic.
        expected = _e_convergents_exact(k)

        # ---------------- mpmath comparison ----------------
        mp.dps = 90
        print("  mpmath test:")
        print("    - working precision set to mp.dps = 90")

        g_mp = prob1.e_cf_mp(dps=90)
        got_mp = _take(g_mp, k)

        for j, (got, exp) in enumerate(zip(got_mp, expected), start=1):
            exp_mpf = mp.mpf(exp.numerator) / mp.mpf(exp.denominator)
            diff = mp.fabs(got - exp_mpf)

            print(f"    convergent {j}:")
            print(f"      approx = {got}")
            print(f"      exact  = {exp_mpf}")
            print(f"      |diff| = {diff}")

            self.assertTrue(
                diff < mp.mpf("1e-70"),
                f"e_cf_mp mismatch at j={j}"
            )

        print("  -> mpmath e convergents match exact oracle\n")

        # ---------------- decimal comparison ----------------
        print("  decimal test:")
        with localcontext() as ctx:
            ctx.prec = 90
            print("    - decimal context precision set to 90")

            g_dec = prob1.e_cf_dec(prec=90)
            got_dec = _take(g_dec, k)

            for j, (got, exp) in enumerate(zip(got_dec, expected), start=1):
                exp_dec = Decimal(exp.numerator) / Decimal(exp.denominator)
                diff = abs(got - exp_dec)

                print(f"    convergent {j}:")
                print(f"      approx = {got}")
                print(f"      exact  = {exp_dec}")
                print(f"      |diff| = {diff}")

                self.assertTrue(
                    diff < Decimal("1e-70"),
                    f"e_cf_dec mismatch at j={j}"
                )

        print("  -> decimal e convergents match exact oracle\n")

# This main block below allows the unit-test file to be run directly as a script:
#
#     $ python cs3430_s26_hw_5_prob_1_uts.py
#
# rather than only through an external test runner.
#
# The special variable __name__ is set to "__main__" when this file
# is executed directly, and to the module name when it is imported.
if __name__ == "__main__":
    # Load all unittest.TestCase classes defined in this module.
    #
    # defaultTestLoader scans the current module and collects every
    # method whose name starts with "test".
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))

    # Create a text-based test runner.
    #
    # verbosity=2 causes unittest to print:
    #   - each test name,
    #   - its pass/fail status,
    # which makes the output easy to follow for students.
    runner = unittest.TextTestRunner(verbosity=2)

    # Run the full test suite and collect the results.
    result = runner.run(suite)

    # Print a clear, student-friendly summary message.
    #
    # We use "!!!" instead of Unicode symbols for compatibility
    # with Ubuntu terminals and plain-text environments.
    if result.wasSuccessful():
        print("\n!!! All HW5 Problem 1 unit tests passed !!!")
    else:
        print("\n!!! Some HW5 Problem 1 unit tests failed !!!")
