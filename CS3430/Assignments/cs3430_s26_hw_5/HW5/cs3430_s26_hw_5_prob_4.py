""" 
Problem 4 Writeup: Large scale expirement

Observations:

This expirement uses extremely fast series for to see how many digits of pi we can compute
with a given precision budget (mp.dps) and a given number of terms. The hash based 
verification allows us to verify the correctness of the digits found in pi_mantissa_99999.txt
without comparing them directly instead your just comparing the hash of the digits.

1) How correctess depends on precision budgeting:

When mp.dps = 250, the chudnovsky result produces the correct 200 digits of pi. However, when
mp.dps = 550, the first hash mismatch occured. This means that mp.dps is insufficient for computing
the full mantissa of pi, however the chudnovsky series will still converge numerically to the
correct value of pi we just did not budget enough precision to get the full mantissa correct.


2) Why increasing mp.dps blindly is not a principled strategy

Blindy turning up mp.dps is not a good idea because that would be a trial and error approach
to finding the right precision budget. This would waste resources, and still fail.

The best strategy is too budget precision based on the expected number of digits of pie that 
you will be able to compute. We need to budget enough precision for the digits we want AND 
a buffer to protect against rounding errors. As we can see from the results, that buffer is not a constant
because 250 was enough for 200 digits, but 550 was not enough for 500 digits.

3) What the hash base verification teaches you about numerical epistemology

Hash base veritifcation allows to verify the correctness without comparing the digits directly. Because,
comparing 2 insanely large strings of digits that are nearly identical is difficult and prone to 
errors. Comparing the hashes of those digits is much easier to compare.

"""
# cs3430_s26_hw_5_prob_4.py
#
# CS3430 S26: Scientific Computing (HW 5, Problem 4)
# Large-scale verification of pi mantissa using
# binary-splitting Chudnovsky + hashing.
# You do not need to write any code here. This is
# for the UTs file used in testing. Quickly scan
# the comments to understand what these functions
# are doing and go to the _uts.py for this problem.
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
# Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
# ------------------------------------------------------------

from typing import Tuple
from mpmath import mp
import hashlib
import argparse

# We reuse the binary-splitting Chudnovsky implementation
# developed in Problem 3.  We import it here to make that dependency
# explicit and unavoidable.
#
# The exact function name must match Problem 3.
from cs3430_s26_hw_5_prob_3 import pi_chudnovsky_bs_mp

# ------------------------------------------------------------
# Representation utility (kept intentionally)
# ------------------------------------------------------------
def pi_mantissa_from_mpf(x: mp.mpf, n_digits: int) -> str:
    """
    Extract the first n_digits of the decimal mantissa of a positive mp.mpf.

    This function performs *no numerical computation*.  It only converts
    a high-precision number into a canonical digit string so that large
    numerical results can be compared using hashes.

    Parameters
    ----------
    x : mp.mpf
        High-precision numerical value of pi.
    n_digits : int
        Number of mantissa digits to extract.

    Returns
    -------
    str
        String of exactly n_digits decimal digits (0–9).
    """
    # Request enough printed digits to include "3." plus the mantissa.
    s = mp.nstr(x, n_digits + 2)

    if "." not in s:
        raise ValueError("Decimal point not found in pi representation.")

    mantissa = s.split(".")[1]
    return mantissa[:n_digits]

# ------------------------------------------------------------
# Hash utility
# ------------------------------------------------------------
def sha256_of_digits(digits: str) -> str:
    """
    Compute SHA-256 hash of a digit string.

    Hashing is used to verify agreement between large numerical artifacts
    without comparing digits individually.
    """
    h = hashlib.sha256()
    h.update(digits.encode("ascii"))
    return h.hexdigest()


# ------------------------------------------------------------
# Main driver
# ------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Verify pi mantissa digits using binary-splitting Chudnovsky "
            "and cryptographic hashing."
        )
    )
    parser.add_argument(
        "ref_file",
        help="Reference file containing decimal mantissa digits of pi"
    )
    parser.add_argument(
        "n_digits",
        type=int,
        help="Number of mantissa digits to verify (N <= 99999)"
    )
    args = parser.parse_args()

    # Import the parser provided earlier in HW 5
    from pi_mantissa_parser import parse_pi_mantissa

    # --------------------------------------------------------
    # Step 1: Read reference mantissa digits
    # --------------------------------------------------------
    ref_digits = parse_pi_mantissa(args.ref_file, args.n_digits)

    # --------------------------------------------------------
    # Step 2: Compute pi using binary-splitting Chudnovsky
    # --------------------------------------------------------
    # Rule of thumb from lecture and Problem 3:
    # ~14 decimal digits per Chudnovsky term.
    terms = (args.n_digits // 14) + 2

    # Guard digits protect against rounding error.
    mp.dps = args.n_digits + 20

    pi_val = pi_chudnovsky_bs_mp(terms=terms, dps=mp.dps)

    # --------------------------------------------------------
    # Step 3: Extract computed mantissa
    # --------------------------------------------------------
    comp_digits = pi_mantissa_from_mpf(pi_val, args.n_digits)

    # --------------------------------------------------------
    # Step 4: Hash comparison
    # --------------------------------------------------------
    ref_hash = sha256_of_digits(ref_digits)
    comp_hash = sha256_of_digits(comp_digits)

    print(f"N digits verified: {args.n_digits}")
    print(f"Reference SHA-256: {ref_hash}")
    print(f"Computed  SHA-256: {comp_hash}")

    if ref_hash == comp_hash:
        print("RESULT: MATCH")
    else:
        print("RESULT: MISMATCH")


if __name__ == "__main__":
    main()
