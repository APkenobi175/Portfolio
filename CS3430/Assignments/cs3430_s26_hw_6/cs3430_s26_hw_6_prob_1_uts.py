# cs3430_s26_hw_6_prob_1_uts.py
# Unit tests for CS3430 S26: Scientific Computing
# HW 6, Problem 1
#
# Our UT CONVENTIONS:
# - We use "!!!" in success messages (Ubuntu/WLS terminal compatibility).
# - We split structural checks and numerical checks into separate tests.

# cs3430_s26_hw_6_prob_1_uts.py

from __future__ import annotations

import unittest
from pathlib import Path
from typing import List

import cs3430_s26_hw_6_prob_1 as hw

class TestHW6Prob1Structural(unittest.TestCase):
    """
    Structural tests verify that required symbols exist
    and that core helper functions satisfy basic contracts.
    """

    def test_required_symbols_exist(self) -> None:
        """
        Ensure that all required public symbols exist in the module.

        This test verifies that students implemented all required
        functions and data structures.
        """
        self.assertTrue(hasattr(hw, "hw6_y_values"))
        self.assertTrue(hasattr(hw, "digit_counts"))
        self.assertTrue(hasattr(hw, "chi_square_statistic"))
        self.assertTrue(hasattr(hw, "chi_square_p_value"))
        self.assertTrue(hasattr(hw, "chi_square_decision"))
        self.assertTrue(hasattr(hw, "run_chi_square_experiments"))
        self.assertTrue(hasattr(hw, "format_results_table"))
        self.assertTrue(hasattr(hw, "ChiSquareRow"))

        print("!!! test_required_symbols_exist passed")

    def test_y_schedule_shape(self) -> None:
        """
        Validate the Y schedule used in HW6.

        Ensures:
        - Starts at 10
        - Ends at 9999
        - Strictly increasing
        """
        ys: List[int] = hw.hw6_y_values()

        print(f"Diagnostic Y schedule (first 10): {ys[:10]}")
        print(f"Diagnostic Y schedule (last 5): {ys[-5:]}")

        self.assertEqual(ys[0], 10)
        self.assertEqual(ys[-1], 9999)
        self.assertTrue(all(ys[i] < ys[i + 1] for i in range(len(ys) - 1)))

        print("!!! test_y_schedule_shape passed")

    def test_digit_counts_contract(self) -> None:
        """
        Verify digit counting behavior.

        Ensures:
        - All digits 0–9 are represented
        - Total count matches string length
        """
        counts = hw.digit_counts("00112233445566778899")

        print(f"Diagnostic counts: {counts}")

        self.assertEqual(sum(counts.values()), 20)
        self.assertEqual(counts[0], 2)
        self.assertEqual(counts[9], 2)

        print("!!! test_digit_counts_contract passed")


class TestHW6Prob1Numerical(unittest.TestCase):
    """
    Numerical tests validate correctness of the chi-square
    implementation and end-to-end experiment execution.
    """

    def test_chi_square_uniform_counts(self) -> None:
        """
        Verify that perfectly uniform counts produce:

            chi^2 = 0
            p-value = 1
            no rejection
        """
        counts = {d: 10 for d in range(10)}

        chi_sq = hw.chi_square_statistic(counts, n=100, k=10)
        p = hw.chi_square_p_value(chi_sq, df=9)
        reject = hw.chi_square_decision(p, alpha=0.05)

        print(f"\nUniform test -> chi^2={chi_sq}, p={p}, reject={reject}")

        self.assertAlmostEqual(chi_sq, 0.0, places=12)
        self.assertAlmostEqual(p, 1.0, places=12)
        self.assertFalse(reject)

        print("!!! test_chi_square_uniform_counts passed")

    def test_chi_square_extreme_counts(self) -> None:
        """
        Verify that extreme deviation produces:

            large chi^2
            tiny p-value
            rejection
        """
        counts = {d: 0 for d in range(10)}
        counts[0] = 100

        chi_sq = hw.chi_square_statistic(counts, n=100, k=10)
        p = hw.chi_square_p_value(chi_sq, df=9)
        reject = hw.chi_square_decision(p, alpha=0.05)

        print(f"\nExtreme test -> chi^2={chi_sq}, p={p}, reject={reject}")

        self.assertAlmostEqual(chi_sq, 900.0, places=12)
        self.assertTrue(p < 1e-10)
        self.assertTrue(reject)

        print("!!! test_chi_square_extreme_counts passed")

    def test_end_to_end_small_run_if_files_present(self) -> None:
        """
        Small integration test with Y = [10, 20, 50].

        Verifies:
        - Proper parsing
        - Valid p-values
        - Boolean decision outputs
        """
        here = Path(__file__).resolve().parent
        pi_file = here / "99_999DigitsOfPi.txt"
        e_file = here / "9_999_DigitsOfE.txt"

        if not pi_file.exists() or not e_file.exists():
            self.skipTest("Reference digit files not found.")

        rows = hw.run_chi_square_experiments(
            pi_reference_filename=str(pi_file),
            e_reference_filename=str(e_file),
            y_values=[10, 20, 50],
            alpha=0.05,
        )

        table = hw.format_results_table(rows)

        print("\n\n===================== DIAGNOSTIC TABLE OUTPUT ==============================")
        print("--------------------------------------------------------------------------------")
        print(table)
        print("--------------------------------------------------------------------------------")
        print("================================================================================\n")

        self.assertEqual(len(rows), 3)

        for r in rows:
            self.assertTrue(0.0 <= r.pi_p_value <= 1.0)
            self.assertTrue(0.0 <= r.e_p_value <= 1.0)
            self.assertIsInstance(r.pi_reject, bool)
            self.assertIsInstance(r.e_reject, bool)

        print("!!! test_end_to_end_small_run_if_files_present passed")

    def test_end_to_end_all_run_if_files_present(self) -> None:
        """
        Full-schedule integration test.

        This test:
          - Uses hw6_y_values() to generate the complete Y schedule.
          - Runs chi-square experiments for all Y values.
          - Prints the full formatted table.
          - Performs structural sanity checks.

        If reference digit files are missing, the test is skipped.
        """

        here = Path(__file__).resolve().parent
        pi_file = here / "99_999DigitsOfPi.txt"
        e_file = here / "9_999_DigitsOfE.txt"

        if not pi_file.exists() or not e_file.exists():
            self.skipTest(
                "Reference digit files not found. "
                "Skipping full integration test."
            )

        ys = hw.hw6_y_values()

        rows = hw.run_chi_square_experiments(
            pi_reference_filename=str(pi_file),
            e_reference_filename=str(e_file),
            y_values=ys,
            alpha=0.05,
        )

        table = hw.format_results_table(rows)

        print("\n\n================== FULL DIAGNOSTIC TABLE OUTPUT ============================")
        print("--------------------------------------------------------------------------------")
        print(table)
        print("--------------------------------------------------------------------------------")
        print("================================================================================\n")
        
        # Structural checks
        self.assertEqual(len(rows), len(ys))

        # Basic sanity checks on every row
        for r in rows:
            self.assertIn(r.num_digits, ys)
            self.assertTrue(0.0 <= r.pi_p_value <= 1.0)
            self.assertTrue(0.0 <= r.e_p_value <= 1.0)
            self.assertIsInstance(r.pi_reject, bool)
            self.assertIsInstance(r.e_reject, bool)

        print("!!! test_end_to_end_all_run_if_files_present passed")

    def test_plot_full_diagnostic_ranges_if_files_present(self) -> None:
        """
        Generate diagnostic plots of p-values across the full Y schedule.

        Produces three PNG files:
            1. 10–3000
            2. 4000–7000
            3. 8000–9999

        Each plot contains:
            - PI p-values (red)
            - E p-values (blue)
            - Alpha threshold line (green)

        No interactive display is shown.
        """

        import matplotlib
        matplotlib.use("Agg")  # Non-interactive backend

        import matplotlib.pyplot as plt

        here = Path(__file__).resolve().parent
        pi_file = here / "99_999DigitsOfPi.txt"
        e_file = here / "9_999_DigitsOfE.txt"

        if not pi_file.exists() or not e_file.exists():
            self.skipTest("Reference digit files not found.")

        ys = hw.hw6_y_values()

        rows = hw.run_chi_square_experiments(
            pi_reference_filename=str(pi_file),
            e_reference_filename=str(e_file),
            y_values=ys,
            alpha=0.05,
        )

        # Convert to lists
        num_digits = [r.num_digits for r in rows]
        pi_pvals = [r.pi_p_value for r in rows]
        e_pvals = [r.e_p_value for r in rows]

        alpha = 0.05

        ranges = [
            (10, 3000, "pvalues_10_to_3000.png"),
            (4000, 7000, "pvalues_4000_to_7000.png"),
            (8000, 9999, "pvalues_8000_to_9999.png"),
        ]

        for lower, upper, filename in ranges:

            # Filter range
            xs = [
                num_digits[i]
                for i in range(len(num_digits))
                if lower <= num_digits[i] <= upper
            ]
            pi_vals = [
                pi_pvals[i]
                for i in range(len(num_digits))
                if lower <= num_digits[i] <= upper
            ]
            e_vals = [
                e_pvals[i]
                for i in range(len(num_digits))
                if lower <= num_digits[i] <= upper
            ]

            if not xs:
                continue

            plt.figure()

            plt.plot(xs, pi_vals, color="red", label="PI p-value")
            plt.plot(xs, e_vals, color="blue", label="E p-value")
            plt.axhline(y=alpha, color="green", linestyle="--", label="Alpha = 0.05")

            plt.xlabel("Number of Digits")
            plt.ylabel("p-value")
            plt.title(f"Chi-Square p-values ({lower}–{upper} digits)")
            plt.legend()

            output_path = here / filename
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close()

        print("!!! test_plot_full_diagnostic_ranges_if_files_present passed")

    def test_plot_small_range_instability_if_files_present(self) -> None:
        """
        Generate a diagnostic plot for the small-sample regime (10–50 digits).

        This plot illustrates instability when expected counts are below 5,
        i.e., when n < 50 for K = 10 categories.

        Produces:
            pvalues_10_to_50_instability.png

        Contains:
            - PI p-values (red, with markers)
            - E p-values (blue, with markers)
            - Alpha threshold line (green dashed)

        No interactive display is shown.
        """

        import matplotlib
        matplotlib.use("Agg")  # Non-interactive backend

        import matplotlib.pyplot as plt

        here = Path(__file__).resolve().parent
        pi_file = here / "99_999DigitsOfPi.txt"
        e_file = here / "9_999_DigitsOfE.txt"

        if not pi_file.exists() or not e_file.exists():
            self.skipTest("Reference digit files not found.")

        ys = hw.hw6_y_values()

        # Restrict to 10–50
        small_range = [y for y in ys if 10 <= y <= 50]

        rows = hw.run_chi_square_experiments(
            pi_reference_filename=str(pi_file),
            e_reference_filename=str(e_file),
            y_values=small_range,
            alpha=0.05,
        )

        num_digits = [r.num_digits for r in rows]
        pi_pvals = [r.pi_p_value for r in rows]
        e_pvals = [r.e_p_value for r in rows]

        alpha = 0.05

        plt.figure()

        plt.plot(
            num_digits,
            pi_pvals,
            color="red",
            marker="o",
            label="PI p-value",
        )

        plt.plot(
            num_digits,
            e_pvals,
            color="blue",
            marker="o",
            label="E p-value",
        )

        plt.axhline(
            y=alpha,
            color="green",
            linestyle="--",
            label="Alpha = 0.05",
        )

        plt.xlabel("Number of Digits")
        plt.ylabel("p-value")
        plt.title("Chi-Square p-values (10–50 digits: Small-Sample Regime)")
        plt.legend()

        output_path = here / "pvalues_10_to_50_instability.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        print("!!! test_plot_small_range_instability_if_files_present passed")

if __name__ == "__main__":
    unittest.main(verbosity=2)
    
