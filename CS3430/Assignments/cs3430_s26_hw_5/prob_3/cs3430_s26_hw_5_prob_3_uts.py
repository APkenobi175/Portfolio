# Unit tests for HW5 Problem 3
# Focus: convergence speed and representation limits (mpmath precision).

import unittest
from mpmath import mp

import cs3430_s26_hw_5_prob_3 as prob3


def _take(gen, n):
    """Consume n values from a generator."""
    return [next(gen) for _ in range(n)]


class TestStructure(unittest.TestCase):
    def test_required_callables_exist(self):
        print("\n[STRUCTURE TEST] Checking required generators for Problem 3")
        self.assertTrue(callable(getattr(prob3, "pi_ramanujan_mp", None)))
        print("  - pi_ramanujan_mp: FOUND and callable")

        self.assertTrue(callable(getattr(prob3, "pi_chudnovsky_bs_mp", None)))
        print("  - pi_chudnovsky_bs_mp: FOUND and callable")

        print("  -> Structural requirements satisfied\n")

    def test_generators_yield_multiple_values(self):
        print("[STRUCTURE TEST] Verifying generators yield multiple values")

        g1 = prob3.pi_ramanujan_mp(dps=80)
        g2 = prob3.pi_chudnovsky_bs_mp(dps=80)

        xs1 = _take(g1, 3)
        xs2 = _take(g2, 3)

        print("  Ramanujan first 3 approximations:", xs1)
        print("  Chudnovsky(BS) first 3 approximations:", xs2)

        self.assertEqual(len(xs1), 3)
        self.assertEqual(len(xs2), 3)

        print("  -> Both generators yield multiple values\n")


class TestConvergence(unittest.TestCase):
    def test_ramanujan_converges_fast(self):
        print("\n[CONVERGENCE TEST] Ramanujan series convergence")

        mp.dps = 80
        pi_ref = mp.pi
        g = prob3.pi_ramanujan_mp(dps=80)

        vals = _take(g, 3)  # 1, 2, 3 terms
        errs = [mp.fabs(v - pi_ref) for v in vals]

        for i, (v, e) in enumerate(zip(vals, errs), start=1):
            print(f"  term_count={i}:")
            print(f"    approx = {mp.nstr(v, 30)}")
            print(f"    |err|  = {mp.nstr(e, 10)}")

        # Expect strong improvement each term.
        self.assertTrue(errs[1] < errs[0])
        self.assertTrue(errs[2] < errs[1])

        # With 80 dps, 2-3 terms should be extremely accurate.
        self.assertTrue(errs[1] < mp.mpf("1e-12"))
        self.assertTrue(errs[2] < mp.mpf("1e-15"))

        print("  -> Ramanujan converges extremely fast\n")

    def test_chudnovsky_bs_converges_even_faster(self):
        print("\n[CONVERGENCE TEST] Chudnovsky (binary splitting) convergence")

        mp.dps = 80
        pi_ref = mp.pi
        g = prob3.pi_chudnovsky_bs_mp(dps=80)

        vals = _take(g, 3)  # 1, 2, 3 terms
        errs = [mp.fabs(v - pi_ref) for v in vals]

        for i, (v, e) in enumerate(zip(vals, errs), start=1):
            print(f"  term_count={i}:")
            print(f"    approx = {mp.nstr(v, 30)}")
            print(f"    |err|  = {mp.nstr(e, 10)}")

        self.assertTrue(errs[1] < errs[0])
        self.assertTrue(errs[2] < errs[1])

        # Chudnovsky is famously ~14 digits per term.
        # With 80 dps, 2-3 terms should push error extremely low.
        self.assertTrue(errs[1] < mp.mpf("1e-25"))
        self.assertTrue(errs[2] < mp.mpf("1e-40"))

        print("  -> Chudnovsky(BS) converges explosively fast\n")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n!!! All HW5 Problem 3 unit tests passed !!!")
    else:
        print("\n!!! Some HW5 Problem 3 unit tests failed !!!")
