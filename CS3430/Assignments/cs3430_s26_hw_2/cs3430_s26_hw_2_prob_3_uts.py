#############################################################
# cs3430_s26_hw_2_prob_3_uts.py
# unit tests for CS3430 S26 HW2 Prob 3
# bugs to vladimir kulyukin in canvas
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
##############################################################

import unittest
import sympy as sp
import numpy as np

from cs3430_s26_hw_2_prob_3 import sp_to_np, sp_cepheid_brightness
from cs3430_s26_hw_2_prob_3 import sp_cepheid_brightness_rate, np_cepheid_brightness
from cs3430_s26_hw_2_prob_3 import plot_cepheid_brightness

class cs3430_s26_hw_2_prob_3_uts(unittest.TestCase):
    """
    Unit tests for Problem 3: Variable Brightness Stars
    """
    def test_01_sp_cepheid_brightness_structural(self):
        print("\n[Test] test_01_sp_cepheid_brightness_structural")
        
        t = sp.Symbol('t', real=True)
        
        expr = sp_cepheid_brightness(t)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        print("[INFO] free symbols:", expr.free_symbols)
        
        print("[CHECK] expr is a SymPy expression (sp.Expr) ...")
        self.assertIsInstance(expr, sp.Expr)
        print("[PASS] expr is a SymPy expression")
        
        print("[CHECK] expr depends on t ...")
        self.assertTrue(expr.has(t))
        print("[PASS] expr depends on t")
        
        print("[CHECK] expr contains sin(...) ...")
        sin_terms = list(expr.atoms(sp.sin))
        print("[INFO] sin terms found:", sin_terms)
        self.assertGreaterEqual(len(sin_terms), 1)
        print("[PASS] expr contains sin(...)")
        
        # Check the argument of sin contains t (we do NOT check exact formula here)
        sin_term = sin_terms[0]
        sin_arg = sin_term.args[0]
        print("[INFO] sin argument =", sin_arg)
        
        print("[CHECK] sin argument depends on t ...")
        self.assertTrue(sin_arg.has(t))
        print("[PASS] sin argument depends on t")
        
        print("[CHECK] expr contains pi ...")
        self.assertTrue(expr.has(sp.pi))
        print("[PASS] expr contains pi")
        
        print("[SUCCESS] test_01_sp_cepheid_brightness_structural PASSED!!!")

    def test_02_sp_cepheid_brightness_numerical(self):
        print("\n[Test] test_02_sp_cepheid_brightness_numerical")

        t = sp.Symbol('t', real=True)
        
        expr = sp_cepheid_brightness(t)
        f_np = sp_to_np(expr)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] f_np type =", type(f_np))
        
        print("[CHECK] NumPy-converted function is callable ...")
        self.assertTrue(callable(f_np))
        print("[PASS] NumPy-converted function is callable")
        
        # Reference brightness function (NumPy version of the model statement)
        def b_ref(tt: float) -> float:
            return 4.0 + 0.35 * np.sin((2.0 * np.pi * tt) / 5.4)

        test_times = [0.0, 1.0, 2.7, 5.4, 10.8]

        for tt in test_times:
            got = float(f_np(tt))
            ref = float(b_ref(tt))
            
            print(f"[INFO] Testing t={tt}")
            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")
            
            # We compare floating-point computations with a tolerance because
            # floating-point arithmetic is approximate.
            self.assertAlmostEqual(got, ref, places=12)
        
        print("[SUCCESS] test_02_sp_cepheid_brightness_numerical PASSED!!!")

    def test_03_sp_cepheid_brightness_rate_structural(self):
        print("\n[Test] test_03_sp_cepheid_brightness_rate_structural")
        
        t = sp.Symbol('t', real=True)
        
        expr = sp_cepheid_brightness_rate(t)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        print("[INFO] free symbols:", expr.free_symbols)
        
        print("[CHECK] expr is a SymPy expression (sp.Expr) ...")
        self.assertIsInstance(expr, sp.Expr)
        print("[PASS] expr is a SymPy expression")
        
        print("[CHECK] expr depends on t ...")
        self.assertTrue(expr.has(t))
        print("[PASS] expr depends on t")
        
        print("[CHECK] expr contains cos(...) ...")
        cos_terms = list(expr.atoms(sp.cos))
        print("[INFO] cos terms found:", cos_terms)
        self.assertGreaterEqual(len(cos_terms), 1)
        print("[PASS] expr contains cos(...)")
        
        print("[CHECK] expr contains pi ...")
        self.assertTrue(expr.has(sp.pi))
        print("[PASS] expr contains pi")
        
        # We expect the derivative to NOT contain a sin term in the final form
        # (it should be proportional to cos(...)), but SymPy sometimes rewrites.
        # So we do not enforce "no sin". We just require "has cos".
        print("[SUCCESS] test_03_sp_cepheid_brightness_rate_structural PASSED!!!")

    def test_04_sp_cepheid_brightness_rate_numerical(self):
        print("\n[Test] test_04_sp_cepheid_brightness_rate_numerical")

        t = sp.Symbol('t', real=True)
        
        expr = sp_cepheid_brightness_rate(t)
        f_np = sp_to_np(expr)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] f_np type =", type(f_np))
        
        print("[CHECK] NumPy-converted function is callable ...")
        self.assertTrue(callable(f_np))
        print("[PASS] NumPy-converted function is callable")
        
        # Reference derivative function (NumPy version of the derivative)
        # This is what the students derive in the math portion of the problem.
        def bderiv_ref(tt: float) -> float:
            return 0.35 * (2.0 * np.pi / 5.4) * np.cos((2.0 * np.pi * tt) / 5.4)

        test_times = [0.0, 1.0, 2.7, 3.0, 5.4]

        for tt in test_times:
            got = float(f_np(tt))
            ref = float(bderiv_ref(tt))
            
            print(f"[INFO] Testing t={tt}")
            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")
            
            # We use a tolerance because floating-point arithmetic is approximate.
            self.assertAlmostEqual(got, ref, places=12)

        # Special: the requested value in the problem statement is at t=1 day
        t1 = 1.0
        got_t1 = float(f_np(t1))
        print("[INFO] dB/dt at t=1 day =", got_t1)

        print("[SUCCESS] test_04_sp_cepheid_brightness_rate_numerical PASSED!!!")

    def test_05_np_cepheid_brightness_structural(self):
        print("\n[Test] test_05_np_cepheid_brightness_structural")
            
        t_vals = np.linspace(0.0, 10.0, 11)
        out = np_cepheid_brightness(t_vals)
        
        print("[INFO] Input type =", type(t_vals))
        print("[INFO] Output type =", type(out))
        print("[INFO] Input shape =", t_vals.shape)
        print("[INFO] Output shape =", out.shape)
        
        print("[CHECK] output is a NumPy array ...")
        self.assertIsInstance(out, np.ndarray)
        print("[PASS] output is a NumPy array")
        
        print("[CHECK] output has the same shape as input ...")
        self.assertEqual(out.shape, t_vals.shape)
        print("[PASS] output has the same shape as input")
        
        print("[CHECK] output dtype is float-like ...")
        self.assertTrue(np.issubdtype(out.dtype, np.floating))
        print("[PASS] output dtype is float-like")
        
        print("[SUCCESS] test_05_np_cepheid_brightness_structural PASSED!!!")

    def test_06_np_cepheid_brightness_numerical(self):
        print("\n[Test] test_06_np_cepheid_brightness_numerical")

        # We test a reasonably fine grid (like what we would use in plotting).
        t_vals = np.linspace(0.0, 90.0, 2000)
        out = np_cepheid_brightness(t_vals)

        print("[INFO] Computed brightness array of length:", len(out))

        print("[CHECK] output min/max are within expected physical bounds ...")
        out_min = float(np.min(out))
        out_max = float(np.max(out))

        print("       min brightness =", out_min)
        print("       max brightness =", out_max)

        # Model: average = 4.0, amplitude = 0.35
        # Expected range is approximately [3.65, 4.35]
        self.assertGreaterEqual(out_min, 3.65 - 1e-3)
        self.assertLessEqual(out_max, 4.35 + 1e-3)

        print("[PASS] output min/max are within expected bounds")

        # Quick spot-check at a few times against the explicit NumPy formula.
        def b_ref(tt: float) -> float:
            return 4.0 + 0.35 * np.sin((2.0 * np.pi * tt) / 5.4)

        test_times = [0.0, 1.0, 2.7, 5.4, 10.8]
        for tt in test_times:
            got = float(np_cepheid_brightness(np.array([tt]))[0])
            ref = float(b_ref(tt))

            print(f"[INFO] Spot-check t={tt}")
            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")

            self.assertAlmostEqual(got, ref, places=12)

        print("[SUCCESS] test_06_np_cepheid_brightness_numerical PASSED!!!")

    # ------------------------------------------------------------------
    # NOTE:
    #
    # These unit tests generate and save brightness plots as PNG files.
    # Plots are visual outputs and are difficult to compare reliably in
    # automated unit tests, so we save them for manual inspection.
    #
    # After running the unit tests, you should see:
    #   - cs3430_s26_hw_2_prob_3_cepheid_brightness_90_days.png
    #   - cs3430_s26_hw_2_prob_3_cepheid_brightness_365_days.png
    #
    # Open these files and confirm you see smooth periodic oscillations.
    # ------------------------------------------------------------------

    def test_07_plot_cepheid_brightness_90_days_png(self):
        print("\n[Test] test_07_plot_cepheid_brightness_90_days_png")

        import os

        t_start = 0.0
        t_end = 90.0
        n = 2000
        
        print("[INFO] Generating Cepheid brightness plot for 90 days ...")
        fig = plot_cepheid_brightness(t_start, t_end, n)
        
        out_png = "cs3430_s26_hw_2_prob_3_cepheid_brightness_90_days.png"
        print("[INFO] Saving plot to:", out_png)
        
        fig.savefig(out_png, dpi=150)
        fig.clf()
        
        print("[CHECK] PNG file exists ...")
        self.assertTrue(os.path.exists(out_png))
        print("[PASS] PNG file exists")
        
        print("[CHECK] PNG file size is non-trivial (> 0 bytes) ...")
        size_bytes = os.path.getsize(out_png)
        print("       size_bytes =", size_bytes)
        self.assertGreater(size_bytes, 0)
        print("[PASS] PNG file size is non-trivial")
        
        print("[SUCCESS] test_07_plot_cepheid_brightness_90_days_png PASSED!!!")


    def test_08_plot_cepheid_brightness_365_days_png(self):
        print("\n[Test] test_08_plot_cepheid_brightness_365_days_png")

        import os
        
        t_start = 0.0
        t_end = 365.0
        n = 5000
        
        print("[INFO] Generating Cepheid brightness plot for 365 days ...")
        fig = plot_cepheid_brightness(t_start, t_end, n)
        
        out_png = "cs3430_s26_hw_2_prob_3_cepheid_brightness_365_days.png"
        print("[INFO] Saving plot to:", out_png)
        
        fig.savefig(out_png, dpi=150)
        fig.clf()
        
        print("[CHECK] PNG file exists ...")
        self.assertTrue(os.path.exists(out_png))
        print("[PASS] PNG file exists")
        
        print("[CHECK] PNG file size is non-trivial (> 0 bytes) ...")
        size_bytes = os.path.getsize(out_png)
        print("       size_bytes =", size_bytes)
        self.assertGreater(size_bytes, 0)
        print("[PASS] PNG file size is non-trivial")
        
        print("[SUCCESS] test_08_plot_cepheid_brightness_365_days_png PASSED!!!")
        
if __name__ == "__main__":
    print("\nRunning CS3430 S26 HW2 Problem 3 unit tests...\n")
    unittest.main(verbosity=2)
    pass

