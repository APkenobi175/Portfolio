# CS3430 S26: Scientific Computing (HW 5, Problem 4 UTs)
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
# Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.


import unittest
from decimal import Decimal
from pathlib import Path
import hashlib

from mpmath import mp

import cs3430_s26_hw_5_prob_4 as prob4

# --------------------------------------------------------------------
# Utility helpers (used only for testing)
# --------------------------------------------------------------------

def _hash_string(s: str) -> str:
    """
    Compute a SHA-256 hash of a digit string.
    Used to compare very long mantissa prefixes efficiently.
    """
    return hashlib.sha256(s.encode("ascii")).hexdigest()


def _read_reference_digits(path: Path, n: int) -> str:
    """
    Read the first n digits from a reference mantissa file.
    Assumes the file contains digits only (no decimal point).
    """
    with open(path, "r", encoding="ascii") as f:
        data = f.read().strip()
    return data[:n]


# --------------------------------------------------------------------
# Tests for utility functions
# --------------------------------------------------------------------

class TestProblem4Utilities(unittest.TestCase):

    def test_mantissa_extraction_basic(self):
        """
        Verify that pi_mantissa_from_mpf extracts the correct digits.
        """
        mp.dps = 80
        x = mp.pi
        digits = prob4.pi_mantissa_from_mpf(x, 50)

        print("[UTILITY TEST] Extracted mantissa:", digits)

        self.assertEqual(
            digits,
            "14159265358979323846264338327950288419716939937510"
        )

    def test_hash_determinism(self):
        """
        Hashing the same digit string twice must produce the same digest.
        """
        s = "1415926535897932384626"
        h1 = _hash_string(s)
        h2 = _hash_string(s)

        print("[HASH TEST] Digest:", h1)

        self.assertEqual(h1, h2)

    def test_hash_sensitivity(self):
        """
        A one-digit change must produce a different hash.
        """
        s1 = "1415926535897932384626"
        s2 = "1415926535897932384627"

        h1 = _hash_string(s1)
        h2 = _hash_string(s2)

        print("[HASH TEST] h1 =", h1)
        print("[HASH TEST] h2 =", h2)

        self.assertNotEqual(h1, h2)


# --------------------------------------------------------------------
# Integration test: Chudnovsky + mantissa extraction + reference check
# --------------------------------------------------------------------

class TestChudnovskyIntegration(unittest.TestCase):

    def test_chudnovsky_produces_correct_prefix(self):
        """
        Verify that the binary-splitting Chudnovsky generator produces
        a mantissa prefix matching the reference digits.

        This test intentionally consumes the generator with next(),
        enforcing the API and usage from Problem 3.
        """
        mp.dps = 120
        terms = 3
        n_digits = 40

        print("[INTEGRATION TEST] Chudnovsky (binary splitting)")
        print(f"  terms    = {terms}")
        print(f"  mp.dps   = {mp.dps}")
        print(f"  digits   = {n_digits}")

        # Consume the generator
        g = prob4.pi_chudnovsky_bs_mp(dps=mp.dps)
        for _ in range(terms):
            pi_bs = next(g)

        bs_digits = prob4.pi_mantissa_from_mpf(pi_bs, n_digits)

        ref_path = Path("pi_mantissa_99999.txt")
        ref_digits = _read_reference_digits(ref_path, n_digits)

        print("  BS digits :", bs_digits)
        print("  Ref digits:", ref_digits)

        self.assertEqual(bs_digits, ref_digits)

class TestChudnovskyDeepConvergence(unittest.TestCase):
    """
    Exploratory test: progressively increase precision, terms, and
    requested mantissa length, and verify correctness via hashing
    against the 99,999-digit reference file.

    This test is intentionally NOT a hard correctness gate.
    Its purpose is to empirically observe where correctness fails on
    your machine.
    """

    def test_hash_matches_until_failure(self):
        import hashlib
        from pathlib import Path

        ref_path = Path("pi_mantissa_99999.txt")
        with open(ref_path, "r", encoding="ascii") as f:
            ref_digits = f.read().strip()

        def sha256(s: str) -> str:
            return hashlib.sha256(s.encode("ascii")).hexdigest()

        # (n_digits, terms, mp.dps)
        configs = [
            (200,    15,   250),
            (500,    40,   550),
            (1000,   75,   1100),
            (2000,   150,  2100),
            (5000,   360,  5200),
            (10000,  720,  10200),
            (20000,  1450, 20500),
            (50000,  3600, 50500),
            (99999,  7200, 101000),
        ]

        print("\n[DEEP CONVERGENCE TEST] Chudnovsky (binary splitting)")
        print("------------------------------------------------------")
        print(f"{'digits':>8} {'terms':>8} {'mp.dps':>10} {'hash match'}")
        print("------------------------------------------------------")

        for n_digits, terms, dps in configs:
            mp.dps = dps

            g = prob4.pi_chudnovsky_bs_mp(dps=mp.dps)
            for _ in range(terms):
                pi_val = next(g)

            computed = prob4.pi_mantissa_from_mpf(pi_val, n_digits)
            reference = ref_digits[:n_digits]

            h_comp = sha256(computed)
            h_ref  = sha256(reference)

            match = (h_comp == h_ref)
            print(f"{n_digits:8d} {terms:8d} {dps:10d} {str(match):>11}")

            if not match:
                print("\n!!! FIRST HASH MISMATCH DETECTED !!!")
                print(f"    n_digits = {n_digits}")
                print(f"    terms    = {terms}")
                print(f"    mp.dps   = {dps}")
                print("    Interpretation:")
                print("      - Chudnovsky series still converges numerically")
                print("      - mp.dps is insufficient for full mantissa correctness")
                break

        print("\n[DEEP CONVERGENCE TEST COMPLETED]")

    def test_my_exploratory_hash_matches(self):
        # I want you to write this test on your own. Write it to experiment
        # with how many digits of the pi mantissa you can reliably squeeze out
        # of your hardware and compare it with the 99,999 digits in the text file.
        # Can you compute all 99,999? That would be AWESOME!
        #
        # The method test_hash_matches_until_failure gives you
        # all the tools you need for this experiment. For example, you can: (1) manually adjust
        # configs parameters in the above test or, which is more fun in my opinion, (2)
        # write nested-for-loops that test ranges of
        # n_digits, terms, mp.dps. The basic question that I want you to think about and
        # experiment with here is, how many digits can I compute with Chudnovsky on my hardware with this
        # number of terms at this level of precision (e.g., mp.dps = 100).
        # There is no right and no wrong here: give yourself an hour to explore, experiment, and report
        # your observations in your write-up at the beginning of
        # cs3430_s26_hw_5_prob_4.py. Have fun!
        pass

# --------------------------------------------------------------------
# Main test runner
# --------------------------------------------------------------------

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n!!! All HW5 Problem 4 unit tests passed !!!")
    else:
        print("\n!!! Some HW5 Problem 4 unit tests failed !!!")

