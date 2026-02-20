from __future__ import annotations

import unittest
from pathlib import Path
from typing import List

import cs3430_s26_hw_6_prob_2 as hw

class TestHW6Prob2Structural(unittest.TestCase):
    """
    Structural tests for HW6 Problem 2.

    These tests verify that required functions/classes exist and that basic
    contracts (types, shapes, and error handling) are respected.
    """

    def test_required_symbols_exist(self) -> None:
        """Verify that the required API symbols exist in the module."""
        required = [
            "fetch_mtDNA_sequence",
            "load_mtDNA_slice",
            "gc_at_encode",
            "acgt_numeric_encode",
            "sliding_window_slices",
            "monobit_test_bits",
            "block_frequency_test_bits",
            "chi_square_gof_4symbol",
            "reject_h0",
            "WindowTestResult",
            "run_sliding_window_analysis",
            "plot_window_pvalues",
            "summarize_rejections",
        ]
        for name in required:
            self.assertTrue(hasattr(hw, name), msg=f"Missing symbol: {name}")

        print("!!! test_required_symbols_exist passed")

    def test_sliding_window_contract(self) -> None:
        """
        Verify sliding window shapes and monotonic start indices.

        We do not test biological correctness here; this is purely a shape contract.
        """
        seq = "ACGT" * 10  # length 40
        windows = hw.sliding_window_slices(seq, window_size=10, step=5)

        starts = [s for s, _ in windows]
        self.assertEqual(starts[0], 0)
        self.assertTrue(all(starts[i] < starts[i + 1] for i in range(len(starts) - 1)))

        for start, w in windows:
            self.assertEqual(len(w), 10)
            self.assertEqual(w, seq[start:start + 10])

        print(f"Diagnostic windows count: {len(windows)}")
        print("!!! test_sliding_window_contract passed")

    def test_encoders_contract(self) -> None:
        """
        Verify that encoders produce correct alphabets and lengths.

        - gc_at_encode returns only 0/1
        - acgt_numeric_encode returns only 1..4
        """
        dna = "ACGTACGTNNNN"
        bits = hw.gc_at_encode(dna)
        vals = hw.acgt_numeric_encode(dna)

        self.assertTrue(all(b in (0, 1) for b in bits))
        self.assertTrue(all(v in (1, 2, 3, 4) for v in vals))

        # N's are ignored by both encoders
        self.assertEqual(len(bits), 8)
        self.assertEqual(len(vals), 8)

        print(f"Diagnostic bits: {bits}")
        print(f"Diagnostic vals: {vals}")
        print("!!! test_encoders_contract passed")


class TestHW6Prob2Numerical(unittest.TestCase):
    """
    Numerical sanity tests for HW6 Problem 2.

    These tests check extreme/simple cases to ensure statistics behave sensibly.
    """

    def test_monobit_extremes(self) -> None:
        """All ones should strongly reject the Bernoulli(1/2) monobit null."""
        bits = [1] * 200
        z, p = hw.monobit_test_bits(bits)
        self.assertTrue(p < 1e-10)

        print(f"\nMonobit extremes -> z={z}, p={p}")
        print("!!! test_monobit_extremes passed")

    def test_chi_square_4symbol_uniform_like(self) -> None:
        """
        A perfectly balanced 4-symbol sample should have chi^2=0 and p=1.

        We construct n=400 with exactly 100 occurrences of each symbol.
        """
        values: List[int] = [1] * 100 + [2] * 100 + [3] * 100 + [4] * 100
        chi_sq, p = hw.chi_square_gof_4symbol(values)

        self.assertAlmostEqual(chi_sq, 0.0, places=12)
        self.assertAlmostEqual(p, 1.0, places=12)

        print(f"\nChiSq 4sym uniform-like -> chi^2={chi_sq}, p={p}")
        print("!!! test_chi_square_4symbol_uniform_like passed")

    def test_end_to_end_slice_and_plot_png(self) -> None:
        """
        End-to-end offline test:
        - Use a fixed mtDNA slice (no network).
        - Run sliding-window analysis with small window/step.
        - Save a PNG plot in the same folder as this UT file.
        - Confirm that the file is created and non-empty.
        """
        dna = hw.load_mtDNA_slice()

        results = hw.run_sliding_window_analysis(
            dna,
            window_size=200,
            step=50,
            block_size=20,
            alpha=0.05,
        )

        self.assertTrue(len(results) > 0)

        # Basic sanity checks on rows
        for r in results:
            self.assertTrue(0.0 <= r.monobit_p_value <= 1.0)
            self.assertTrue(0.0 <= r.block_p_value <= 1.0)
            self.assertTrue(0.0 <= r.chi4_p_value <= 1.0)

        here = Path(__file__).resolve().parent
        out_png = here / "hw6_prob2_slice_pvalues.png"

        hw.plot_window_pvalues(results, filename=str(out_png), alpha=0.05)

        self.assertTrue(out_png.exists())
        self.assertTrue(out_png.stat().st_size > 0)

        rates = hw.summarize_rejections(results)
        print("\nRejection rates (slice):", rates)
        print(f"Saved plot: {out_png}")
        print("!!! test_end_to_end_slice_and_plot_png passed")


    def test_full_genome_sliding_window_rejections_if_file_present(self) -> None:
        """
        Full-genome integration test using mtDNA_sequence.txt.

        This test:
          - Loads the full mitochondrial genome sequence from file.
          - Runs sliding-window randomness tests under:
                (1) GC/AT binary encoding
                (2) 4-symbol categorical encoding
          - Prints rejection rates for each test.
          - Performs structural sanity checks.

        If mtDNA_sequence.txt is missing, the test is skipped.
        """

        from pathlib import Path

        here = Path(__file__).resolve().parent
        genome_file = here / "mtDNA_sequence.txt"

        if not genome_file.exists():
            self.skipTest("mtDNA_sequence.txt not found. Skipping full-genome test.")

        # --- Load full genome ---
        with open(genome_file, "r", encoding="utf-8") as f:
            dna = f.read().strip().upper()

        self.assertTrue(len(dna) > 10000)  # sanity check
        print(f"\nFull genome length: {len(dna)}")

        # --- Parameters ---
        window_size = 500
        step = 50
        alpha = 0.05

        # --- Run sliding-window experiment ---
        rows = hw.run_sliding_window_analysis(
            dna,
            window_size=window_size,
            step=step,
            alpha=alpha,
        )

        self.assertTrue(len(rows) > 0)

        # --- Compute rejection rates ---
        total = len(rows)

        monobit_rej = sum(r.monobit_reject for r in rows)
        block_rej = sum(r.block_reject for r in rows)
        chi4_rej = sum(r.chi4_reject for r in rows)

        rejection_summary = {
            "monobit": monobit_rej / total,
            "block": block_rej / total,
            "chi4": chi4_rej / total,
        }

        print("\n=== FULL GENOME REJECTION RATES ===")
        print(f"Window size = {window_size}, step = {step}, alpha = {alpha}")
        print(f"Total windows: {total}")
        print("Rejection rates:", rejection_summary)
        print("====================================\n")

        # --- Structural checks ---
        for r in rows:
            self.assertTrue(0.0 <= r.monobit_p_value <= 1.0)
            self.assertTrue(0.0 <= r.block_p_value <= 1.0)
            self.assertTrue(0.0 <= r.chi4_p_value <= 1.0)

        print("!!! test_full_genome_sliding_window_rejections_if_file_present passed")

    def test_full_genome_rejection_table_if_file_present(self) -> None:
        """
        Verify that formatted rejection summary table is generated
        correctly for the full genome, if the file is present.
        """

        here = Path(__file__).resolve().parent
        genome_file = here / "mtDNA_sequence.txt"

        if not genome_file.exists():
            self.skipTest("mtDNA_sequence.txt not found.")

        with open(genome_file, "r", encoding="utf-8") as f:
            dna = f.read().strip()

        results = hw.run_sliding_window_analysis(
            dna_sequence=dna,
            window_size=500,
            step=50,
            block_size=25,
            alpha=0.05,
        )

        table = hw.format_rejection_summary_table(results)

        print("\n=== FULL GENOME REJECTION SUMMARY TABLE ===")
        print(table)
        print("============================================\n")

        self.assertIn("Sliding Window Rejection Summary", table)
        self.assertTrue(len(results) > 0)

        print("!!! test_full_genome_rejection_table_if_file_present passed")

    def test_full_genome_plots_if_file_present(self) -> None:
        """
        Generate full-genome p-value plots if mtDNA_sequence.txt is present.
        """

        here = Path(__file__).resolve().parent
        genome_file = here / "mtDNA_sequence.txt"

        if not genome_file.exists():
            self.skipTest("mtDNA_sequence.txt not found.")

        with open(genome_file, "r", encoding="utf-8") as f:
            dna = f.read().strip()

        results = hw.run_sliding_window_analysis(
            dna_sequence=dna,
            window_size=500,
            step=50,
            block_size=25,
            alpha=0.05,
        )
        
        hw.save_full_genome_pvalue_plots(
            results,
            alpha=0.05,
            prefix="hw6_prob2_full",
        )

        print("Saved full genome p-value plots.")

        self.assertTrue(len(results) > 0)

        print("!!! test_full_genome_plots_if_file_present passed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
