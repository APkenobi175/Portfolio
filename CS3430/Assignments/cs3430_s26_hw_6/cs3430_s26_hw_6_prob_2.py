"""
Problem 2 Write Up
Ammon Phipps

1) Why the 4 symbol null fails everywhere

    My Results:
        Test Type        | Rejections | Rate
        ---------------------------------------
        Monobit (GC/AT)  |        215 | 0.668
        Block Frequency  |        143 | 0.444
        Chi^2 (A,C,G,T)  |        322 | 1.000
        ---------------------------------------

    The 4 symbol chi square tests rejects the null hypothesis every time because
    mitochondrial DNA is not uniformily distrubuted across all 4 A, C, G, and T.
    With window size W = 500, we expect 125 counts of each base 1/4 for each base, but thats not reality.
    Counts are not close to 125. This is because GC content varies across the genome and some regions are more AT rich while others are more GC rich. 

2) Why monobit oscillates

    The monobit test oscillates because it is checking for GC content to be at 50% in each window
    The monobit rejection rate is 66.8% which is higher then the expected 5%. This indicates that the GC content 
    varies across a genome while some are closer to 50% and fail to reject, most are far from 50% and reject.
    This causes the data to oscillate.

3) How encoding affects statistical conclusions

    The encoding affects the statistical conclusions because we are interpreting the data under different models. DNA testing may be more compatible
    with different null models. For example under the monobit test the results are different because its mostly sensitive to the GC/AT balance,
    but under the block frequency test the results are different and the 4 symbol null hypothesis is drastically different because it is checking for the distrubution of
    all 4 bases. This demonstrates that randomness tests aren't testing the data itself, but testing them with encoding and the model.

    This can show us that some data may be better tested under different models

4) How this contrasts with the behavior of pi and e

    This contrasts with pi and e because the null hypothesis failed to reject for both pi and e a majority of the time with only one rejection. 

"""

"""
CS3430 S26 - HW6 Problem 2 (DNA Randomness Demo via Sliding Windows)

I hope this module will demonstrate a core scientific computing lesson:

  Randomness tests do NOT test "the data itself."
  They test a representation (aka encoding) of the data under a 
  stochastic model.

Here, we use the human mitochondrial reference genome (NC_012920.1) and apply
randomness tests to sliding windows of the sequence under two encodings:

  1) Binary encoding (GC/AT):
       G,C -> 1
       A,T -> 0
     Tests:
       - Monobit test (Z-test)
       - Block frequency test (chi-square)

  2) 4-symbol encoding (A,C,G,T -> 1,2,3,4)
     Test:
       - Chi-square goodness-of-fit against the UNIFORM model:
           P(A)=P(C)=P(G)=P(T)=1/4

Important interpretation reminders:

- Rejecting H0 does NOT mean "DNA is non-random in an absolute sense."
  It means "DNA is inconsistent with THIS null model for THIS encoding
  on THIS window size and step."

- Failing to reject H0 does NOT prove randomness.

- Expected-count conditions matter:
    For a chi-square GOF test with K categories, a common rule-of-thumb
    is that each expected count should be >= 5.
    For K=4 (ACGT uniform), expected count is n/4, so we want n >= 20.
    For K=10 (decimal digits), expected count is n/10, so we want n >= 50.
  When expected counts are smaller, p-values can be unstable and the test
  becomes technically unreliable.

This file is designed to be unit-test friendly and reproducible:
- It contains no plotting display calls (no plt.show()).
- Plot functions save PNGs to disk. No run-time display.

Copyright (C) Vladimir Kulyukin. All rights reserved.
For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Sequence

from collections import Counter

import matplotlib.pyplot as plt
import requests
from scipy.stats import chi2, norm

def load_mtDNA_slice() -> str:
    """
    Return a short, fixed slice (~300-400 bp) from the human mtDNA reference genome.

    This keeps demos reproducible and ensures unit tests can run offline.

    Returns
    -------
    str
        Uppercase DNA string over {A,C,G,T}.
    """
    return (
        "GATCACAGGTCTATCACCCTATTAACCACTCACGGGAGCTCTCCATGCAT"
        "TTGGTATTTTCGTCTGGGGGGTGTGCACGCGATAGCATTGCGAGACGCTG"
        "GAGCCGGAGCACCCTATGTCGCAGTATCTGTCTTTGATTCCTGCCTCATT"
        "CTATTATTTATCGCACCTACGTTCAATATTACAGGCGAACATACCTACTA"
        "AAGTGTGTTAATTAATTAATGCTTGTAGGACATAATAATAACAATTGAAT"
        "GTCTGCACAGCCACTTTCCACACAGACATCATAACAAAAAATTTCCACC"
    )


def gc_at_encode(dna: str) -> list[int]:
    """
    Encode DNA as a bit sequence:
      G,C -> 1
      A,T -> 0

    Parameters
    ----------
    dna : str
        Input DNA string.

    Returns
    -------
    list[int]
        Encoded bits.

    Notes
    -----
    - Non-ACGT symbols (e.g., N) are ignored (not encoded).
    """
    bits: list[int] = []
    for base in dna.upper():
        if base in ("G", "C"):
            bits.append(1)
        elif base in ("A", "T"):
            bits.append(0)
        else:
            # Ignore ambiguous symbols (N, etc.)
            pass
    return bits


def acgt_numeric_encode(dna: str) -> list[int]:
    """
    Encode DNA bases numerically:
      A -> 1, C -> 2, G -> 3, T -> 4

    Parameters
    ----------
    dna : str
        Input DNA string.

    Returns
    -------
    list[int]
        Numeric encoding over {1,2,3,4}.

    Notes
    -----
    - Non-ACGT symbols are ignored.
    """
    mapping: dict[str, int] = {"A": 1, "C": 2, "G": 3, "T": 4}
    return [mapping[b] for b in dna.upper() if b in mapping]


def sliding_window_slices(sequence: str, window_size: int, step: int) -> list[tuple[int, str]]:
    """
    Generate sliding windows (overlapping) over a DNA string.

    Parameters
    ----------
    sequence : str
        Full DNA sequence.
    window_size : int
        Number of bases in each window.
    step : int
        Step size between consecutive windows.

    Returns
    -------
    list[tuple[int, str]]
        A list of (start_index, window_string) with 0-based start indices.

    Raises
    ------
    ValueError
        If window_size <= 0, step <= 0, or window_size > len(sequence).
    """
    if window_size <= 0:
        raise ValueError("window_size must be positive.")
    if step <= 0:
        raise ValueError("step must be positive.")
    if window_size > len(sequence):
        raise ValueError("window_size cannot exceed sequence length.")

    windows: list[tuple[int, str]] = []
    for start in range(0, len(sequence) - window_size + 1, step):
        windows.append((start, sequence[start:start + window_size]))
    return windows


#TODO:
def monobit_test_bits(bits: Sequence[int]) -> tuple[float, float]:
    """
    Monobit test for a binary sequence under H0: i.i.d. Bernoulli(1/2).

    Test statistic:
      S = sum(bits)  (number of ones)
      Z = (S - n/2) / sqrt(n/4)
      p = 2 * P(Z >= |z|)  (two-sided)

    Parameters
    ----------
    bits : Sequence[int]
        Sequence of 0/1 values.

    Returns
    -------
    tuple[float, float]
        (z_statistic, p_value)

    Raises
    ------
    ValueError
        If the input sequence is empty or contains non-binary values.
    """
    n = len(bits)
    if n == 0:
        raise ValueError("bits must be non-empty.")
    if any(b not in (0, 1) for b in bits):
        raise ValueError("bits must contain only 0/1 values.")

    # Compute the total number of 1s in the bit sequence.
    #
    # Under the null hypothesis H0:
    #   Bits are i.i.d. Bernoulli(1/2)
    #
    # the expected number of 1s in n trials is n/2.
    #
    # 1) We explicitly cast to float to ensure downstream arithmetic
    # is performed in floating-point.
    s = float(sum(bits))

    # 2) The theoretical mean of a Binomial(n, 1/2) random variable:
    #
    #     E[S] = n * (1/2) = n / 2
    # compute E[S] and save it in the variable mean.
    #
    mean = n / 2.0
    
    # 3) The theoretical variance of a Binomial(n, 1/2):
    #
    #     Var(S) = n * p * (1 - p)
    #            = n * (1/2) * (1/2)
    #            = n / 4
    #
    # This is the variance of the count of 1s.
    # Compute Var(S) and save it in the variable var.
    # 
    var = n / 4.0
    
    # 4) Compute the z-statistic:
    #
    #     z = (observed - expected) / sqrt(variance)
    #
    # Under H0 and for sufficiently large n,
    # this statistic is approximately standard normal (N(0,1)).
    #
    # This is the classical normal approximation to the binomial.
    # Compute the z statistic and save it in variable mean. Remember
    # that observed in our case is s and expected is mean.
    #
    z = (s - mean) / var ** 0.5

    # 5) Compute a two-sided p-value.
    #
    # norm.sf(x) computes the survival function:
    #     P(Z >= x)
    #
    # For a two-sided test we compute:
    #     2 * P(|Z| >= |z|)
    #
    # which equals:
    #     2 * norm.sf(|z|)
    #
    # Small p-values indicate significant imbalance between
    # zeros and ones.
    # Compute the p-value as 2 * norm.sf(abs(z)) and save it
    # in variable p.
    #
    p = 2 * norm.sf(abs(z))

    # 6) Return both the z-statistic and the p-value.
    #
    # Interpretation:
    #   - Large |z|  → strong deviation from 50/50 balance
    #   - Small p    → reject Bernoulli(1/2) null
    return z, float(p)

#TODO:    
def block_frequency_test_bits(bits: Sequence[int], block_size: int) -> tuple[float, float]:
    """
    Block frequency test (NIST-style idea) for a binary sequence under
    H0: i.i.d. Bernoulli(1/2).

    Split into N = floor(n / M) non-overlapping blocks of size M.
    For each block i, compute pi_i = (#ones in block i) / M.
    Statistic:
      chi^2 = 4M * sum_{i=1..N} (pi_i - 1/2)^2
    Under H0 (approx), chi^2 ~ chi^2_{N}.

    Parameters
    ----------
    bits : Sequence[int]
        Binary sequence of 0/1.
    block_size : int
        Block length M.

    Returns
    -------
    tuple[float, float]
        (chi_square_statistic, p_value)

    Raises
    ------
    ValueError
        If bits empty, contains non-binary values, or block_size invalid.
    """
    n = len(bits)
    if n == 0:
        raise ValueError("bits must be non-empty.")
    if any(b not in (0, 1) for b in bits):
        raise ValueError("bits must contain only 0/1 values.")
    if block_size <= 0:
        raise ValueError("block_size must be positive.")
    if block_size > n:
        raise ValueError("block_size cannot exceed sequence length.")

    m = block_size
    num_blocks = n // m
    if num_blocks == 0:
        raise ValueError("Not enough data for even one full block.")

    # 1) Initialize an accumulator for the block deviations.
    #
    # We will sum squared deviations of block proportions from 1/2.
    # This corresponds to measuring how far each block's empirical
    # frequency of 1s deviates from the Bernoulli(1/2) expectation.
    total = 0.0

    # 2) Iterate over each block.
    #
    # num_blocks is typically:
    #     floor(n / m)
    #
    # where:
    #   n = total number of bits
    #   m = block size
    #
    # Each block is analyzed independently.
    for i in range(num_blocks):

        # 2a) Extract the i-th block.
        #
        # For block size m:
        #   block 0 → bits[0:m]
        #   block 1 → bits[m:2m]
        #   block 2 → bits[2m:3m]
        #   ...
        #
        # This slicing enforces disjoint blocks.
        block = bits[i * m:(i + 1) * m]

        # Compute the empirical proportion of 1s in this block.
        #
        # pi_i = (# of 1s in block) / m
        #
        # Under H0 (Bernoulli(1/2)):
        #     E[pi_i] = 1/2
        # Compute the value of pi_i as sum(block) divided by m
        # and save it in variable pi_i.
        #
        pi_i = sum(block) / m

        # 2b) Accumulate the squared deviation from 1/2.
        #
        # We measure how much this block's proportion deviates
        # from the theoretical expectation 0.5.
        #
        # Large deviations increase evidence against H0.
        # Update the total by adding (pi_i - 0.5)^2 to it.
        #
        total += (pi_i - 0.5) ** 2

    # 3) Convert the accumulated deviations into a chi-square statistic.
    #
    # The classical block frequency test statistic is:
    #
    #     X^2 = 4m * sum_{i=1}^{num_blocks} (pi_i - 1/2)^2
    #
    # Why 4m?
    #
    # Because under H0:
    #     Var(pi_i) = (1/4) / m
    #
    # so scaling by 4m normalizes the statistic so that,
    # asymptotically, it follows a chi-square distribution
    # with df = num_blocks.
    # Compute chi_sq as the product of 4.0, m, and total.
    # and save is in variable chi_sq
    #
    chi_sq = 4.0 * m * total

    # 4) Compute the p-value using the chi-square survival function.
    #
    # df = num_blocks
    #
    # Large chi_sq → small p-value → reject H0.
    #
    # Important:
    # This test assumes:
    #   - Blocks are independent
    #   - m is sufficiently large
    #   - Expected counts per block are not too small
    # Compute the p value with chi2.sf(chi_sq, df=num_blocks)
    # and save it in variable p.
    #
    p = chi2.sf(chi_sq, df=num_blocks)

    # 5) Return the chi-square statistic and its p-value.
    #
    # Interpretation:
    #   - If p <= alpha → reject Bernoulli(1/2)
    #   - If p > alpha  → fail to reject
    #
    # This test detects local imbalance across blocks,
    # even when global balance (monobit) holds.
    return float(chi_sq), float(p)

def chi_square_gof_4symbol(values: Sequence[int]) -> tuple[float, float]:
    """
    Chi-square goodness-of-fit test for values in {1,2,3,4} under the uniform null:
      H0: P(1)=P(2)=P(3)=P(4)=1/4, i.i.d.

    Statistic:
      chi^2 = sum_{k=1..4} (O_k - E)^2 / E,  where E = n/4

    Under H0 (approx, for large n), chi^2 ~ chi^2_{3}.

    Parameters
    ----------
    values : Sequence[int]
        Sequence over {1,2,3,4}.

    Returns
    -------
    tuple[float, float]
        (chi_square_statistic, p_value)

    Raises
    ------
    ValueError
        If sequence empty or contains values outside {1,2,3,4}.
    """
    n = len(values)
    if n == 0:
        raise ValueError("values must be non-empty.")
    if any(v not in (1, 2, 3, 4) for v in values):
        raise ValueError("values must contain only 1,2,3,4.")

    counts = Counter(values)
    expected = n / 4.0

    # Initialize chi-square accumulator.
    #
    # We will compute:
    #
    #     X^2 = sum_{i=1}^4 (O_i - E_i)^2 / E_i
    #
    # where:
    #   O_i = observed count of base i
    #   E_i = expected count under uniform null
    chi_sq = 0.0
    

    # Iterate over the four DNA symbols encoded as:
    #   1 → A
    #   2 → C
    #   3 → G
    #   4 → T
    #
    # Under the null hypothesis:
    #     H0: P(A)=P(C)=P(G)=P(T)=1/4
    #
    # So each symbol has expected frequency n/4.
    for symbol in (1, 2, 3, 4):

        # Retrieve observed count for this symbol.
        #
        # counts is typically a Counter object.
        #
        # If a symbol does not appear at all,
        # counts.get(symbol, 0) safely returns 0.
        observed = counts.get(symbol, 0)

        # Add this symbol’s contribution to the chi-square statistic.
        #
        # (observed - expected)^2 / expected
        #
        # Interpretation:
        #   - Large deviation from expected → larger contribution
        #   - Zero deviation → contributes 0
        #
        # Because expected = n/4, the reliability condition
        # E_i ≥ 5 becomes:
        #
        #     n ≥ 20
        #
        # which is comfortably satisfied in typical window sizes.
        chi_sq += (observed - expected) ** 2 / expected


    # Compute p-value using chi-square survival function.
    #
    # Degrees of freedom:
    #
    #     df = k - 1 = 4 - 1 = 3
    #
    # We subtract 1 because the counts must sum to n,
    # which imposes one linear constraint.
    #
    # Large chi_sq → small p-value → reject uniformity.
    p = chi2.sf(chi_sq, df=3)
    
    # Return chi-square statistic and p-value.
    #
    # Interpretation:
    #
    #   - p ≤ alpha → reject uniform base composition
    #   - p > alpha → fail to reject uniformity
    #
    # Important:
    # This test detects global compositional imbalance only.
    # It does NOT detect spatial structure or periodicity.
    return float(chi_sq), float(p)

#TODO:
def reject_h0(p_value: float, alpha: float) -> bool:
    """
    Decision rule shared across tests:
      Reject H0 iff p_value <= alpha.

    Parameters
    ----------
    p_value : float
        Computed p-value in [0,1].
    alpha : float
        Significance level (risk tolerance), typically 0.05.

    Returns
    -------
    bool
        True if reject H0, False otherwise.
    """
    # Return a boolean testing if p_value <= alpha.
    
    return p_value <= alpha


# Let's make this immutable.
@dataclass(frozen=True)
class WindowTestResult:
    """
    Results for one sliding window.

    start_index is 0-based genomic position of the window start.
    """
    start_index: int
    window_size: int

    monobit_p_value: float
    block_p_value: float
    chi4_p_value: float

    monobit_reject: bool
    block_reject: bool
    chi4_reject: bool

# the workhorse!
def run_sliding_window_analysis(
    dna_sequence: str,
    *,
    window_size: int = 500,
    step: int = 50,
    block_size: int = 25,
    alpha: float = 0.05,
) -> list[WindowTestResult]:
    """
    Perform sliding-window tests over a DNA sequence.

    Per window:
      1) Binary GC/AT encoding:
           - monobit p-value
           - block frequency p-value (with provided block_size)
      2) 4-symbol A,C,G,T encoding:
           - chi-square GOF p-value under uniform null

    Parameters
    ----------
    dna_sequence : str
        Full DNA sequence.
    window_size : int
        Window length W (default 500).
    step : int
        Step size between windows (default 50).
    block_size : int
        Block size for the binary block-frequency test.
        A natural default is 25, giving 20 blocks when window_size=500.
    alpha : float
        Significance level.

    Returns
    -------
    list[WindowTestResult]
        Results in increasing order of start_index.

    Notes
    -----
    - Expected-count reliability:
        * For chi-square on A,C,G,T with W=500, expected count is 125 per base under uniform,
          so the expected-count rule-of-thumb is comfortably satisfied.
        * For block frequency, df = floor(W/block_size). With W=500 and block_size=25,
          df=20: normal approximations are typically reasonable.
    """
    windows = sliding_window_slices(dna_sequence, window_size, step)
    results: list[WindowTestResult] = []

    for start, window in windows:
        bits = gc_at_encode(window)
        z_mono, p_mono = monobit_test_bits(bits)

        chi_block, p_block = block_frequency_test_bits(bits, block_size=block_size)

        vals = acgt_numeric_encode(window)
        chi4, p_chi4 = chi_square_gof_4symbol(vals)

        results.append(
            WindowTestResult(
                start_index=start,
                window_size=window_size,
                monobit_p_value=float(p_mono),
                block_p_value=float(p_block),
                chi4_p_value=float(p_chi4),
                monobit_reject=reject_h0(float(p_mono), alpha),
                block_reject=reject_h0(float(p_block), alpha),
                chi4_reject=reject_h0(float(p_chi4), alpha),
            )
        )

    return results

# formation tool.
def format_rejection_summary_table(
    results: list[WindowTestResult]
) -> str:
    """
    Format a rejection summary table for sliding-window DNA analysis.

    Parameters
    ----------
    results : list[WindowTestResult]
        Output of run_sliding_window_analysis().

    Returns
    -------
    str
        A formatted ASCII summary table.

    Notes
    -----
    - Rejection rate = (# rejected windows) / (total windows).
    - This is purely descriptive.
    - Interpretation must consider alpha and window count.
    """

    if not results:
        raise ValueError("Results list must not be empty.")

    total = len(results)

    mono_rej = sum(r.monobit_reject for r in results)
    block_rej = sum(r.block_reject for r in results)
    chi4_rej = sum(r.chi4_reject for r in results)

    mono_rate = mono_rej / total
    block_rate = block_rej / total
    chi4_rate = chi4_rej / total

    # Please, Snake, let these floats align nicely!
    # I am bit tired of typing.
    header = (
        "Sliding Window Rejection Summary\n"
        f"Window size = {results[0].window_size}, "
        f"Total windows = {total}\n\n"
        "Test Type        | Rejections | Rate\n"
        "---------------------------------------"
    )

    lines = [
        header,
        f"Monobit (GC/AT)  | {mono_rej:10d} | {mono_rate:5.3f}",
        f"Block Frequency  | {block_rej:10d} | {block_rate:5.3f}",
        f"Chi^2 (A,C,G,T)  | {chi4_rej:10d} | {chi4_rate:5.3f}",
        "---------------------------------------",
    ]

    return "\n".join(lines)

def plot_window_pvalues(
    results: Sequence[WindowTestResult],
    *,
    filename: str,
    alpha: float = 0.05,
) -> None:
    """
    Save a PNG plot of p-values vs genomic position (start_index).

    Lines:
      - monobit p-values (red)
      - block frequency p-values (blue)
      - 4-symbol chi-square p-values (black)
      - alpha threshold (green)

    Parameters
    ----------
    results : Sequence[WindowTestResult]
        Results from run_sliding_window_analysis().
    filename : str
        Output PNG filename.
    alpha : float
        Significance level line to draw.

    Returns
    -------
    None

    Notes
    -----
    - This function saves the figure and closes it.
    - It does not display anything.
    """
    xs = [r.start_index for r in results]
    p_mono = [r.monobit_p_value for r in results]
    p_block = [r.block_p_value for r in results]
    p_chi4 = [r.chi4_p_value for r in results]
    alpha_line = [alpha for _ in results]

    plt.figure()
    plt.plot(xs, p_mono, label="Monobit p-value (GC/AT)", color="red")
    plt.plot(xs, p_block, label="BlockFreq p-value (GC/AT)", color="blue")
    plt.plot(xs, p_chi4, label="ChiSq p-value (A,C,G,T)", color="black")
    plt.plot(xs, alpha_line, label=f"alpha = {alpha}", color="green")

    plt.xlabel("Window start index (0-based)")
    plt.ylabel("p-value")
    plt.title("Sliding-window p-values on mtDNA")
    plt.ylim(-0.02, 1.02)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.close()


def summarize_rejections(
    results: Sequence[WindowTestResult],
) -> dict[str, float]:
    """
    Summarize rejection rates across windows for each test.

    Parameters
    ----------
    results : Sequence[WindowTestResult]
        Window results.

    Returns
    -------
    dict[str, float]
        Fraction of windows rejecting H0 for each test:
          {"monobit": ..., "block": ..., "chi4": ...}
    """
    n = len(results)
    if n == 0:
        return {"monobit": 0.0, "block": 0.0, "chi4": 0.0}

    return {
        "monobit": sum(r.monobit_reject for r in results) / n,
        "block": sum(r.block_reject for r in results) / n,
        "chi4": sum(r.chi4_reject for r in results) / n,
    }

def save_full_genome_pvalue_plots(
    results: list[WindowTestResult],
    *,
    alpha: float,
    prefix: str = "hw6_prob2_full",
) -> None:
    """
    Save p-value plots for full-genome sliding-window analysis.

    Parameters
    ----------
    results : list[WindowTestResult]
        Output of run_sliding_window_analysis().
    alpha : float
        Significance level (plotted as horizontal reference line).
    prefix : str
        Filename prefix for saved PNGs.

    Notes
    -----
    Generates:
      - {prefix}_monobit.png
      - {prefix}_block.png
      - {prefix}_chi4.png
      - {prefix}_combined.png
    """

    if not results:
        raise ValueError("Results must not be empty.")

    positions = [r.start_index for r in results]
    mono = [r.monobit_p_value for r in results]
    block = [r.block_p_value for r in results]
    chi4 = [r.chi4_p_value for r in results]

    # --- Monobit plot ---
    plt.figure(figsize=(10, 4))
    plt.plot(positions, mono, color="red", label="Monobit (GC/AT)")
    plt.axhline(alpha, color="green", linestyle="--", label="alpha")
    plt.title("Full Genome Sliding Window: Monobit Test")
    plt.xlabel("Genome Position (window start)")
    plt.ylabel("p-value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{prefix}_monobit.png")
    plt.close()

    # --- Block plot ---
    plt.figure(figsize=(10, 4))
    plt.plot(positions, block, color="blue", label="Block Frequency")
    plt.axhline(alpha, color="green", linestyle="--", label="alpha")
    plt.title("Full Genome Sliding Window: Block Frequency Test")
    plt.xlabel("Genome Position (window start)")
    plt.ylabel("p-value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{prefix}_block.png")
    plt.close()

    # --- Chi4 plot ---
    plt.figure(figsize=(10, 4))
    plt.plot(positions, chi4, color="purple", label="Chi^2 (A,C,G,T)")
    plt.axhline(alpha, color="green", linestyle="--", label="alpha")
    plt.title("Full Genome Sliding Window: 4-Symbol Chi-Square Test")
    plt.xlabel("Genome Position (window start)")
    plt.ylabel("p-value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{prefix}_chi4.png")
    plt.close()

    # --- Combined plot ---
    plt.figure(figsize=(12, 5))
    plt.plot(positions, mono, color="red", label="Monobit")
    plt.plot(positions, block, color="blue", label="Block")
    plt.plot(positions, chi4, color="purple", label="Chi4")
    plt.axhline(alpha, color="green", linestyle="--", label="alpha")
    plt.title("Full Genome Sliding Window: All Tests")
    plt.xlabel("Genome Position (window start)")
    plt.ylabel("p-value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{prefix}_combined.png")
    plt.close()

##################################################
#    PASTING THIS HERE SO THE UNIT TEST WORKS    #
##################################################
def fetch_mtDNA_sequence() -> str:
    """
    Fetch the human mitochondrial reference genome (NC_012920.1)
    from NCBI in FASTA format and return the raw DNA sequence
    (without FASTA header or line breaks).

    Returns
    -------
    str
        A single uppercase DNA string of length 16569.
    """
    params = {
        "id": ACCESSION,
        "db": "nuccore",
        "report": "fasta",
        "retmode": "text",
    }

    response = requests.get(NCBI_URL, params=params, timeout=10)
    response.raise_for_status()

    fasta_text = response.text.splitlines()

    # Remove FASTA header (first line begins with '>')
    sequence_lines = [line.strip() for line in fasta_text if not line.startswith(">")]

    sequence = "".join(sequence_lines).upper()

    return sequence



if __name__ == "__main__":
    # Lightweight offline demo: run on a fixed slice and save one PNG.
    dna = load_mtDNA_slice()
    res = run_sliding_window_analysis(dna, window_size=200, step=20, block_size=20, alpha=0.05)
    plot_window_pvalues(res, filename="mtdna_slice_pvalues.png", alpha=0.05)
    print("Saved: mtdna_slice_pvalues.png")
    print("Rejection rates:", summarize_rejections(res))
