"""
===========================================================
autocorr_analysis.py

Autocorrelation analysis for CS3430 S26 Project 1.

This file does autocorrelation testing for hive temperature
and weight data using selected lags and optional detrending.
-- bugs to vladimir kulyukin in canvas.

NO # YOUR CODE HERE IN THIS FILE. 

Design principles:
- data_processing.py contains transformations and statistics.
- This file handles detrending (raw, global, diurnal), bulldozing,
  and reporting via table.
- Defaults are defined via keywords but customizable for research.

Copyright (C) Vladimir Kulyukin. All rights reserved.
For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
==============================================================
"""

from typing import List
import numpy as np

from data_processing import (
    load_series,
    detrend_global,
    detrend_diurnal,
    autocorrelation,
    autocorrelation_test,
)

# ==========================================================
# Defaults (core assignment requirements)
# ==========================================================

DEFAULT_ALPHA = 0.05
DEFAULT_LAGS = [1, 2, 3, 24]
DEFAULT_DETREND_TYPES = ["raw", "global", "diurnal"]

# ==========================================================
# Helper: Apply detrending
# ==========================================================

def _apply_detrending(
    timestamps: list,
    y: np.ndarray,
    detrend_type: str
) -> np.ndarray:
    """
    Apply selected detrending to a sequence.

    Parameters
    ----------
    timestamps : list
        List of datetime timestamps.
    y : np.ndarray
        Numerical sequence.
    detrend_type : str
        One of {"raw", "global", "diurnal"}.

    Returns
    -------
    y_processed : np.ndarray
        Possibly detrended sequence.
    """

    if detrend_type == "raw":
        return y

    elif detrend_type == "global":
        return detrend_global(y)

    elif detrend_type == "diurnal":
        return detrend_diurnal(timestamps, y)

    else:
        raise ValueError("Invalid detrend_type.")


# ==========================================================
# Helper: Compute results for selected lags
# ==========================================================

def _compute_autocorr_results(
    y: np.ndarray,
    lags: List[int],
    alpha: float
) -> List[tuple]:
    """
    Compute rho, p-value, and decision for each lag.

    Returns
    -------
    results : list of tuples
        (lag, rho, p_value, decision_bool)
    """

    results = []

    for lag in lags:
        rho = autocorrelation(y, lag)
        _, p_value = autocorrelation_test(y, lag)

        # Decision: True = Fail to reject H0
        decision = p_value > alpha

        results.append((lag, rho, p_value, decision))

    return results


# ==========================================================
# Helper: Print formatted table
# ==========================================================

def _print_table(
    hive_id: int,
    direction: str,
    variable_name: str,
    n: int,
    alpha: float,
    detrend_type: str,
    results: List[tuple]
) -> None:
    """
    Print formatted autocorrelation table.
    """

    print(f"\n=== AUTOCORRELATION TABLE ===")
    print(f"Hive: {hive_id} | Direction: {direction} | Variable: {variable_name}")
    print(f"n = {n} | alpha = {alpha}\n")

    print("Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected")
    print("----------------------------------------------------------")

    for lag, rho, p_value, decision in results:
        print(
            f"{lag:>3} | "
            f"{detrend_type:<10} | "
            f"{rho:>8.4f} | "
            f"{p_value:>8.4f} | "
            f"{str(decision):<5}"
        )

    print("----------------------------------------------------------")


# ==========================================================
# Main Bulldozer
# ==========================================================

def run_autocorr_analysis(
    csv_path: str,
    alpha: float = DEFAULT_ALPHA,
    lags: List[int] = DEFAULT_LAGS,
    detrend_types: List[str] = DEFAULT_DETREND_TYPES
) -> None:
    """
    Run autocorrelation analysis on hive CSV file.

    Parameters
    ----------
    csv_path : str
        Path to hive CSV file.
    alpha : float
        Significance level.
    lags : list of int
        Lags to test.
    detrend_types : list of str
        Detrending types to apply (raw, global, diurnal).
    """

    data = load_series(csv_path)

    for (hive_id, direction), series in data.items():

        for variable_name in ["temp", "weight"]:

            timestamps, y = series[variable_name]

            if len(y) == 0:
                continue

            y = np.asarray(y, dtype=float)
            n = len(y)

            for detrend_type in detrend_types:

                y_processed = _apply_detrending(
                    timestamps,
                    y,
                    detrend_type
                )

                results = _compute_autocorr_results(
                    y_processed,
                    lags,
                    alpha
                )

                _print_table(
                    hive_id,
                    direction,
                    variable_name,
                    n,
                    alpha,
                    detrend_type,
                    results
                )
