"""
Problem 3 Writeup
Ammon Phipps


1) Addressing the behavior of the 256-symbol uniform model

    in the 256-symbol uniform model, pixel intesnties are i.i.d. uniform on {0,...,255}. This means that each pixel is equally
    likely to take on any of the 256 possible intensity values, and the value of one pixel does not influence the value of any other
    pixel. The chi-square test checks whether the distribution of pixel intensities is different from the uniform distribution.
    If the p-value is below the alpha, we reject the null hypothesis, which indicates that the image has a non-uniform histogram.

    Truly random images should fail to reject the null hypothesis (95% of the time), while natural images have more non-uniform histograms due to lighting, textures, etc.
    For a natural image we expect to reject the uniform model, while for a truly random image we would fail to reject it.

2) Addressing the behavior of the binary Monobit model

    The monobit tests checks whetgher the proportion of pixels >=128 is close to 1/2. True random images mostly fail to reject the null hypothesis (95% of the time)
    However, a black and white image with exactly 50% black and 50% white pixels would pass the monobit test, even though it is not random at all. 
    Natural images might reject the null hypothesis of the monobit test because they often have more light or dark pixels, leading to a proportion that is not 1/2

3) Addressing the behavior of the binary block frequency model

    This test, checks whether BLOCKS of pixels are close to 50/50. so this test is similar to the monobit test, but it detects cluistering. True random images should fail to reject the null hypothesis (95% of the time)
    because the local blocks should also have a 50/50 distrubution. 

    even if the image fails to rejrect in the monobit test, it can still fail to reject in the block test if there are clusters of light or dark pixels. for example, in the globally balanced
    spatially structured image, the monobit test would fail to reject because it is globally balanced, but the block frequency test would reject because there are large blocks of light and dark pixels.
    
        Image is globally balanced but spatially structured. ... Half-black/half-white result:
        ImageRandomnessResult(n_pixels=10000, chi256_p_value=0.0, monobit_p_value=1.0, block_p_value=0.0, chi256_reject=True, monobit_reject=False, block_reject=True)

"""









#############################################################
# cs3430_s26_hw_6_prob_3.py
# HW6 Problem 3: Image Randomness Experiments
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
# Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
#############################################################

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
import math


#############################################################
# Image I/O (matplotlib only)
#############################################################

def load_grayscale_image(path: str) -> np.ndarray:
    """
    Load an image using matplotlib and convert to grayscale if needed.

    Returns
    -------
    np.ndarray
        Float array with values in [0, 255].
    """
    I = plt.imread(path)

    if I.ndim == 3:
        I = I[..., :3]
        I = np.mean(I, axis=2)

    if I.max() <= 1.0:
        I = I * 255.0

    return I.astype(float)

def save_grayscale_image(I: np.ndarray, path: str) -> None:
    """
    Save a grayscale image using matplotlib.
    """
    plt.imsave(
        path,
        np.clip(I, 0, 255),
        cmap="gray",
        vmin=0,
        vmax=255
    )

#############################################################
# Random Image Generator
#############################################################

#TODO:
def generate_random_image(
    height: int,
    width: int,
    seed: int | None = None
) -> np.ndarray:
    """
    Generate a synthetic random grayscale image.

    Pixel intensities are integers in [0,255].

    Parameters
    ----------
    height : int
    width : int
    seed : int | None
        Seed for reproducibility.

    Returns
    -------
    np.ndarray
        Float array of shape (height, width).
    """
    # 1) Save the random generator in variable rng by
    # by computing it as np.random.default_rng(seed).
    #
    rng = np.random.default_rng(seed)
    #
    # 2) Compute the image I as
    # rng.integers(0, 256, size=(height, width), dtype=np.uint8)
    #
    I = rng.integers(0, 256, size=(height, width), dtype=np.uint8)
    #
    # 3) return the image I
    return I.astype(float)


#############################################################
# Encodings
#############################################################

def flatten_image(I: np.ndarray) -> np.ndarray:
    """
    Flatten image into a 1D array.
    """
    return I.reshape(-1)

def binarize_image(
    I: np.ndarray,
    threshold: float = 128.0
) -> np.ndarray:
    """
    Binarize grayscale image.

    < threshold  -> 0
    >= threshold -> 1
    """
    return (I >= threshold).astype(int).reshape(-1)


#############################################################
# Statistical Tests
#############################################################

def chi_square_gof_256(intensities: np.ndarray) -> Tuple[float, float]:
    """
    Chi-square goodness-of-fit test for 256 grayscale levels.

    Null hypothesis:
        Intensities are i.i.d. uniform on {0,...,255}.
    """
    # Determine number of pixels in the flattened image.
    #
    # intensities is assumed to be a 1D NumPy array of grayscale values
    # in {0, 1, ..., 255}.
    #
    # n = total number of categorical observations.
    n = len(intensities)


    # Guard against invalid input.
    #
    # A chi-square test requires at least one observation.
    # With n = 0, the statistic is undefined.
    if n == 0:
        raise ValueError("Empty intensity sequence.")

    
    # Count occurrences of each grayscale level.
    #
    # np.bincount counts frequencies of non-negative integers.
    #
    # minlength=256 ensures that every possible intensity
    # from 0 to 255 has a slot — even if some never appear.
    #
    # This is crucial because the chi-square test requires
    # explicit counts for all categories.
    counts = np.bincount(intensities.astype(int), minlength=256)

    # Under the null hypothesis:
    #
    #     H0: Intensities are i.i.d. Uniform({0,...,255})
    #
    # Each grayscale level has probability 1/256.
    #
    # Therefore expected count per level is:
    #
    #     E_i = n / 256
    #
    expected = n / 256.0


    # Compute chi-square statistic in vectorized form.
    #
    # Formula:
    #
    #     X^2 = sum_{i=0}^{255} (O_i - E_i)^2 / E_i
    #
    # where:
    #   O_i = observed count for intensity i
    #   E_i = expected count
    #
    # Large deviations from uniformity increase X^2.
    chi_sq = np.sum((counts - expected) ** 2 / expected)


    # Compute p-value using chi-square survival function.
    #
    # Degrees of freedom:
    #
    #     df = k - 1 = 256 - 1 = 255
    #
    # We subtract 1 because counts must sum to n,
    # which imposes one linear constraint.
    #
    # Large chi_sq → small p-value → reject uniformity.
    p_value = chi2.sf(chi_sq, df=255)


    # Return chi-square statistic and p-value as floats.
    #
    # Interpretation:
    #
    #   - p_value ≤ alpha → reject uniform grayscale model
    #   - p_value > alpha → fail to reject uniformity
    #
    # Important:
    #   - This test checks global histogram uniformity only.
    #   - It does NOT test spatial structure.
    #   - An image can have perfectly uniform histogram
    #     yet still be highly structured (e.g., checkerboard).
    #
    return float(chi_sq), float(p_value)


def monobit_test_bits(bits: np.ndarray) -> Tuple[float, float]:
    """
    Monobit test for binary sequence.
    """
    n = len(bits)
    if n == 0:
        raise ValueError("Empty bit sequence.")

    S = np.sum(bits)
    z = (S - n/2) / math.sqrt(n/4)
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z)/math.sqrt(2))))

    return float(z), float(p)


def block_frequency_test_bits(
    bits: np.ndarray,
    block_size: int
) -> Tuple[float, float]:
    """
    Block frequency chi-square test for binary sequence.
    """
    n = len(bits)
    if block_size <= 0:
        raise ValueError("block_size must be positive.")

    num_blocks = n // block_size
    if num_blocks == 0:
        raise ValueError("Block size too large.")

    chi_sq = 0.0

    for i in range(num_blocks):
        block = bits[i*block_size:(i+1)*block_size]
        pi_hat = np.mean(block)
        chi_sq += 4 * block_size * (pi_hat - 0.5) ** 2

    p_value = chi2.sf(chi_sq, df=num_blocks)

    return float(chi_sq), float(p_value)


#############################################################
# Unified Analysis
#############################################################

# @dataclass automatically generates:
#   - __init__()
#   - __repr__()
#   - equality comparison
#
# This allows us to store structured statistical results
# in a clean, immutable-style container.
#
# Conceptually:
#   This class represents the complete statistical profile
#   of one image under multiple randomness models.
@dataclass
class ImageRandomnessResult:

    # Total number of pixels in the flattened image.
    # This is the sample size n used in statistical tests.
    n_pixels: int

    # p-value from 256-level chi-square test.
    # Tests whether grayscale intensities are uniform
    # over {0,...,255}.
    chi256_p_value: float

    # p-value from monobit test after binarization.
    # Tests whether proportion of pixels >= 128
    # equals 0.5.
    monobit_p_value: float

    # p-value from block-frequency test on binary encoding.
    # Tests whether local blocks deviate from 50/50 structure.
    block_p_value: float

    # Boolean decision for 256-level chi-square test.
    # True if p ≤ alpha (reject uniform grayscale model).
    chi256_reject: bool

    # Boolean decision for monobit test.
    monobit_reject: bool

    # Boolean decision for block-frequency test.
    block_reject: bool


def analyze_image_randomness(
    I: np.ndarray,
    *,
    block_size: int = 100,
    alpha: float = 0.05
) -> ImageRandomnessResult:
    """
    Perform grayscale and binarized randomness tests.

    Parameters
    ----------
    I : np.ndarray
        Grayscale image (2D array).
        Values expected in [0, 255].

    block_size : int
        Block size for block-frequency test
        applied to binary encoding.

    alpha : float
        Significance level for hypothesis testing.

    Returns
    -------
    ImageRandomnessResult
        Structured statistical summary.
    """

    # Flatten the 2D image into a 1D array.
    #
    # Statistical tests treat data as sequences.
    # Spatial structure is ignored here —
    # this is purely frequency-based inference.
    #
    # If image is M x N:
    #     flat has length M*N.
    flat = flatten_image(I)


    # Convert grayscale image to binary encoding.
    #
    # Rule:
    #   intensity < 128  → 0
    #   intensity ≥ 128 → 1
    #
    # This creates a Bernoulli-style bit sequence.
    #
    # IMPORTANT:
    # This is a modeling choice.
    # Different encodings lead to different statistical behavior.
    bits = binarize_image(I)


    # --- 256-level chi-square test ---
    #
    # Tests:
    #
    #     H0: Intensities are i.i.d. uniform on {0,...,255}
    #
    # df = 255
    #
    # Sensitive to global histogram imbalance.
    chi256_stat, chi256_p = chi_square_gof_256(flat)


    # --- Monobit test on binary encoding ---
    #
    # Tests:
    #
    #     H0: bits ~ i.i.d. Bernoulli(1/2)
    #
    # Equivalent to testing whether proportion of
    # light pixels equals 50%.
    #
    # Only tests global balance, not structure.
    _, mono_p = monobit_test_bits(bits)


    # --- Block-frequency test on binary encoding ---
    #
    # Divides bit sequence into blocks of size m.
    #
    # Tests whether local proportions deviate
    # from 50% in each block.
    #
    # Sensitive to clustering and structure.
    _, block_p = block_frequency_test_bits(bits, block_size)


    # Construct structured result object.
    #
    # Decision rule:
    #
    #     Reject H0  if p ≤ alpha
    #
    # Note:
    #   This is model-based inference.
    #   Rejecting does NOT mean "non-random" in an absolute sense.
    #
    # It means:
    #   "Data unlikely under this null model."
    #
    return ImageRandomnessResult(
        n_pixels=len(flat),

        chi256_p_value=chi256_p,
        monobit_p_value=mono_p,
        block_p_value=block_p,

        chi256_reject=(chi256_p <= alpha),
        monobit_reject=(mono_p <= alpha),
        block_reject=(block_p <= alpha),
    )

#############################################################
# Table Formatter
#############################################################

def format_image_randomness_table(
    results: Dict[str, ImageRandomnessResult]
) -> str:
    """
    Format results into an ASCII table.
    """
    header = (
        "Image                | Pixels | Chi256 p | Monobit p | Block p | "
        "Chi256 Reject | Mono Reject | Block Reject\n"
        "---------------------------------------------------------------------------------------------"
    )

    lines = [header]

    for name, r in results.items():
        lines.append(
            f"{name:20} | "
            f"{r.n_pixels:6d} | "
            f"{r.chi256_p_value:9.4f} | "
            f"{r.monobit_p_value:9.4f} | "
            f"{r.block_p_value:8.4f} | "
            f"{str(r.chi256_reject):13} | "
            f"{str(r.monobit_reject):11} | "
            f"{str(r.block_reject):12}"
        )

    return "\n".join(lines)
