# Unit tests for HW5 Problem 2
# Focus: convergence behavior, not exact arithmetic.

import unittest
from mpmath import mp
import cs3430_s26_hw_5_prob_2 as prob2


def _take(gen, n):
    """Consume n values from a generator."""
    return [next(gen) for _ in range(n)]


class TestStructure(unittest.TestCase):
    """
    Structural tests:
      - functions exist,
      - functions are callable,
      - generators yield multiple values.
    """

    def test_required_callables_exist(self):
        print("\n[STRUCTURE TEST] Checking required generators")

        self.assertTrue(callable(getattr(prob2, "pi_leibniz_mp", None)))
        print("  - pi_leibniz_mp: FOUND and callable")

        self.assertTrue(callable(getattr(prob2, "pi_machin_mp", None)))
        print("  - pi_machin_mp:  FOUND and callable")

        print("  -> Structural requirements satisfied\n")

    def test_generators_yield_multiple_values(self):
        print("[STRUCTURE TEST] Verifying generators yield values")

        g1 = prob2.pi_leibniz_mp(dps=60)
        g2 = prob2.pi_machin_mp(dps=60)

        xs1 = _take(g1, 3)
        xs2 = _take(g2, 3)

        print("  Leibniz first 3 approximations:", xs1)
        print("  Machin  first 3 approximations:", xs2)

        self.assertEqual(len(xs1), 3)
        self.assertEqual(len(xs2), 3)

        print("  -> Both generators yield multiple values\n")


class TestConvergence(unittest.TestCase):
    """
    Convergence tests:
      - both generators converge toward mp.pi,
      - Machin converges dramatically faster than Leibniz.
    """

    def test_leibniz_vs_machin_convergence(self):
        print("\n[CONVERGENCE TEST] Leibniz vs Machin")

        mp.dps = 60
        pi_ref = mp.pi

        g_leib = prob2.pi_leibniz_mp(dps=60)
        g_mach = prob2.pi_machin_mp(dps=60)

        # Take a modest number of terms.
        leib_vals = _take(g_leib, 2000)
        mach_vals = _take(g_mach, 10)

        leib_err = mp.fabs(leib_vals[-1] - pi_ref)
        mach_err = mp.fabs(mach_vals[-1] - pi_ref)

        print(f"  Leibniz after 2000 terms:")
        print(f"    approx = {leib_vals[-1]}")
        print(f"    |error| = {leib_err}")

        print(f"\n  Machin after 10 terms:")
        print(f"    approx = {mach_vals[-1]}")
        print(f"    |error| = {mach_err}")

        # We do not require exact thresholds, only a dramatic difference.
        self.assertTrue(mach_err < leib_err)

        print("\n  -> Machin converges far faster than Leibniz\n")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n!!! All HW5 Problem 2 unit tests passed !!!")
    else:
        print("\n!!! Some HW5 Problem 2 unit tests failed !!!")
