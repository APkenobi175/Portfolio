#############################################################
# cs3430_s26_hw_6_prob_3_uts.py
#############################################################

from __future__ import annotations

import unittest
import os
import numpy as np
import matplotlib.pyplot as plt

import cs3430_s26_hw_6_prob_3 as hw


class TestHW6Prob3Structural(unittest.TestCase):

    def test_required_symbols_exist(self) -> None:
        self.assertTrue(hasattr(hw, "generate_random_image"))
        self.assertTrue(hasattr(hw, "analyze_image_randomness"))
        self.assertTrue(hasattr(hw, "format_image_randomness_table"))
        print("!!! test_required_symbols_exist passed")

    def test_random_image_reproducible(self) -> None:
        I1 = hw.generate_random_image(10, 10, seed=42)
        I2 = hw.generate_random_image(10, 10, seed=42)
        self.assertTrue(np.array_equal(I1, I2))
        print("!!! test_random_image_reproducible passed")


class TestHW6Prob3Numerical(unittest.TestCase):

    def test_uniform_256_balanced(self) -> None:
        vals = np.repeat(np.arange(256), 10)
        chi, p = hw.chi_square_gof_256(vals)
        self.assertAlmostEqual(chi, 0.0)
        self.assertAlmostEqual(p, 1.0)
        print("!!! test_uniform_256_balanced passed")

    def test_random_image_end_to_end(self) -> None:
        I = hw.generate_random_image(100, 100, seed=1)
        result = hw.analyze_image_randomness(I)

        print("\n=== RANDOM IMAGE TEST ===")
        print(result)

        self.assertTrue(0.0 <= result.chi256_p_value <= 1.0)
        self.assertTrue(0.0 <= result.monobit_p_value <= 1.0)
        self.assertTrue(0.0 <= result.block_p_value <= 1.0)

        print("!!! test_random_image_end_to_end passed")

    def test_real_images_if_present(self) -> None:
        """
        Optional integration test.
        Runs only if imgs/ directory exists.
        """
        if not os.path.exists("imgs"):
            self.skipTest("imgs directory not found.")

        results = {}

        for fname in os.listdir("imgs"):
            path = os.path.join("imgs", fname)
            I = hw.load_grayscale_image(path)
            results[fname] = hw.analyze_image_randomness(I)

        table = hw.format_image_randomness_table(results)

        print("\n=== REAL IMAGE RANDOMNESS TABLE ===")
        print(table)
        print("====================================\n")

        self.assertTrue(len(results) > 0)

        print("!!! test_real_images_if_present passed")

    def test_constant_image_rejects_everything(self) -> None:
        """
        A constant grayscale image should strongly reject all randomness tests.
        The image is saved for visual inspection.
        """

        print("\nSTART: test_constant_image_rejects_everything")

        I = np.zeros((100, 100), dtype=float)

        # Save image
        plt.imsave("constant_image.png", I, cmap="gray", vmin=0, vmax=255)

        result = hw.analyze_image_randomness(I)

        print("Constant image result:")
        print(result)

        self.assertTrue(result.chi256_reject)
        self.assertTrue(result.monobit_reject)
        self.assertTrue(result.block_reject)

        print("Saved: constant_image.png")
        print("PASS !!! test_constant_image_rejects_everything")

    def test_half_black_half_white_structure(self) -> None:
        """
        Image is globally balanced but spatially structured.
        Saved for visual inspection.
        """

        print("\nSTART: test_half_black_half_white_structure")

        I = np.zeros((100, 100), dtype=float)
        I[50:, :] = 255.0

        plt.imsave("half_black_half_white.png", I, cmap="gray", vmin=0, vmax=255)

        result = hw.analyze_image_randomness(I, block_size=100)

        print("Half-black/half-white result:")
        print(result)

        self.assertTrue(result.chi256_reject)
        self.assertTrue(result.block_reject)
        self.assertTrue(0.0 <= result.monobit_p_value <= 1.0)

        print("Saved: half_black_half_white.png")
        print("PASS !!! test_half_black_half_white_structure")

    def test_checkerboard_image(self) -> None:
        """
        Generate a 100x100 checkerboard image.

        This image is:
          - Globally balanced
          - Highly structured locally
          - Periodic

        It should strongly reject most randomness tests.
        """

        print("\nSTART: test_checkerboard_image")

        I = np.zeros((100, 100), dtype=float)

        for i in range(100):
            for j in range(100):
                if (i + j) % 2 == 0:
                    I[i, j] = 0.0
                else:
                    I[i, j] = 255.0

        plt.imsave("checkerboard_100x100.png", I, cmap="gray", vmin=0, vmax=255)

        result = hw.analyze_image_randomness(I, block_size=100)

        print("Checkerboard result:")
        print(result)

        # 256-level uniform should reject
        self.assertTrue(result.chi256_reject)

        # Block test may FAIL TO REJECT because each 100-pixel row is perfectly balanced.
        # This demonstrates dependence on block alignment.
        self.assertTrue(0.0 <= result.block_p_value <= 1.0)

        # Monobit may or may not reject depending on threshold
        self.assertTrue(0.0 <= result.monobit_p_value <= 1.0)

        print("Saved: checkerboard_100x100.png")
        print("PASS !!! test_checkerboard_image")


    def test_checkerboard_image_misaligned_blocks(self) -> None:
        """
        Checkerboard with misaligned block size (37).
        
        Even when block size does not align with row boundaries,
        the checkerboard pattern remains locally balanced at nearly
        every scale because it alternates 0/1 at the pixel level.
        
        This demonstrates an important limitation:
        
        The block frequency test detects local imbalance,
        NOT periodic deterministic structure.
        
        Therefore:
        - 256-level chi-square must reject (only two gray levels used).
        - Monobit should fail to reject (exact 50/50 balance).
        - Block test may also fail to reject because each block
          remains nearly perfectly balanced.
        """

        print("\nSTART: test_checkerboard_image_misaligned_blocks")


        # Construct 100x100 checkerboard
        I = np.fromfunction(lambda i, j: ((i + j) % 2) * 255, (100, 100))
        I = I.astype(float)
        
        result = hw.analyze_image_randomness(I, block_size=37, alpha=0.05)
        
        print("Checkerboard (misaligned blocks) result:")
        print(result)
        
        # 256-level uniform must reject (only 2 of 256 levels used)
        self.assertTrue(result.chi256_reject)
        
        # Monobit should NOT reject (exact 50/50 balance)
        self.assertFalse(result.monobit_reject)
        
        # Block test may fail to reject because local balance persists
        self.assertTrue(0.0 <= result.block_p_value <= 1.0)

        print("PASS !!! test_checkerboard_image_misaligned_blocks")
        
        
if __name__ == "__main__":
    unittest.main(verbosity=2)
