#############################################################
# cs3430_s26_hw_2_prob_1_uts.py
# unit tests for CS3430 S26 HW2 Prob 1
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

from cs3430_s26_hw_2_prob_1 import sp_b, sp_to_np, sp_ice_cream_area, sp_cone_area, sp_ice_cream_rat, sp_ice_cream_rat_limit

class cs3430_s26_hw_2_prob_1_uts(unittest.TestCase):
    """
    Unit tests for Problem 1: Ice Cream Cone Problem.
    """

    def test_01_sp_b_structural(self):
        print("\n[Test] test_01_sp_b_structural")
        th = sp.Symbol('theta', positive=True, real=True)
        a  = sp.Symbol('a', positive=True, real=True)
        
        expr = sp_b(th, a)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        
        # --- Type check ---
        print("[CHECK] expr is a SymPy Mul ...")
        self.assertIsInstance(expr, sp.core.mul.Mul)
        print("[PASS] expr is a SymPy Mul")
        
        # --- Must depend on both a and theta ---
        print("[CHECK] expr depends on theta ...")
        self.assertTrue(expr.has(th))
        print("[PASS] expr depends on theta")
        
        print("[CHECK] expr depends on a ...")
        self.assertTrue(expr.has(a))
        print("[PASS] expr depends on a")
        
        # --- Must contain exactly one sine term ---
        sin_terms = list(expr.atoms(sp.sin))
        print("[INFO] sin terms found:", sin_terms)
        
        print("[CHECK] exactly 1 sin term exists ...")
        self.assertEqual(len(sin_terms), 1)
        print("[PASS] exactly 1 sin term exists")
        
        # --- sin argument must be theta/2 ---
        sin_arg = sin_terms[0].args[0]
        print("[INFO] sin argument =", sin_arg)
        
        print("[CHECK] sin argument simplifies to theta/2 ...")
        self.assertEqual(sp.simplify(sin_arg - th/2), 0)
        print("[PASS] sin argument is theta/2")
        
        # --- Must contain 'a' as a symbol ---
        print("[INFO] free symbols:", expr.free_symbols)
        
        print("[CHECK] 'a' is among free symbols ...")
        self.assertIn(a, expr.free_symbols)
        print("[PASS] 'a' is among free symbols")
        
        print("[SUCCESS] test_01_sp_b_structural PASSED!!!")

    def test_02_sp_to_np_on_sp_b_numerical(self):
        print("\n[Test] test_02_sp_to_np_on_sp_b_numerical")
        th = sp.Symbol('theta', positive=True, real=True)
        a  = sp.Symbol('a', positive=True, real=True)
        
        # Step 1: build symbolic expression
        b_expr = sp_b(th, a)
        print("[INFO] b_expr =", b_expr)
        
        # Step 2: convert to NumPy callable
        b_np = sp_to_np(b_expr)
        print("[INFO] b_np type =", type(b_np))
        
        print("[CHECK] b_np is callable ...")
        self.assertTrue(callable(b_np))
        print("[PASS] b_np is callable")
        
        # Step 3: numerical tests
        # (a, theta) test cases
        test_cases = [
            (1.0, 0.1),
            (2.0, 0.2),
            (3.5, 0.5),
            (10.0, 1.0),
        ]

        for aval, thval in test_cases:
            print(f"[INFO] Testing a={aval}, theta={thval}")
            
            # b_np takes arguments in sorted symbol order: (a, theta)
            # because vars_sorted = sorted(expr.free_symbols, key=lambda s: s.name)
            got = float(b_np(aval, thval))
            
            # Numerical reference value (computed directly with NumPy, not symbolically)
            ref = float(2.0 * aval * np.sin(thval / 2.0))

            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")

            # We use assertAlmostEqual() because the computations are done in
            # floating-point arithmetic. Even if two formulas are mathematically
            # identical, their numerical results may differ by a tiny rounding error.
            #
            # places=12 means we require agreement up to 12 digits after the decimal
            # point (i.e., the absolute difference should be about 1e-12 or smaller).
            #
            # In other words, we don't demand exact equality of floats, only that
            # the results are numerically consistent to high precision.            
            self.assertAlmostEqual(got, ref, places=12)

        print("[SUCCESS] test_02_sp_to_np_on_sp_b_numerical PASSED!!!")

    def test_03_sp_ice_cream_area_structural(self):
        print("\n[Test] test_03_sp_ice_cream_area_structural")
        th = sp.Symbol('theta', positive=True, real=True)
        a  = sp.Symbol('a', positive=True, real=True)
        
        expr = sp_ice_cream_area(th, a)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        print("[INFO] free symbols:", expr.free_symbols)
        
        # --- Type check ---
        print("[CHECK] expr is a SymPy Mul ...")
        self.assertIsInstance(expr, sp.core.mul.Mul)
        print("[PASS] expr is a SymPy Mul")
        
        # --- Must depend on both theta and a ---
        print("[CHECK] expr depends on theta ...")
        self.assertTrue(expr.has(th))
        print("[PASS] expr depends on theta")
        
        print("[CHECK] expr depends on a ...")
        self.assertTrue(expr.has(a))
        print("[PASS] expr depends on a")
        
        # --- Must contain pi ---
        print("[CHECK] expr contains pi ...")
        self.assertTrue(expr.has(sp.pi))
        print("[PASS] expr contains pi")
        
        # --- Must contain sin term(s) ---
        sin_terms = list(expr.atoms(sp.sin))
        print("[INFO] sin terms found:", sin_terms)
        
        print("[CHECK] at least 1 sin term exists ...")
        self.assertGreaterEqual(len(sin_terms), 1)
        print("[PASS] at least 1 sin term exists")
        
        # --- Must contain sin(theta/2) somewhere ---
        found_sin_theta_over_2 = False
        for s in sin_terms:
            if sp.simplify(s.args[0] - th/2) == 0:
                found_sin_theta_over_2 = True
                break

            print("[CHECK] sin argument includes theta/2 ...")
            self.assertTrue(found_sin_theta_over_2)
            print("[PASS] sin argument includes theta/2")

        print("[SUCCESS] test_03_sp_ice_cream_area_structural PASSED!!!")

    def test_04_sp_ice_cream_area_numerical(self):
        print("\n[Test] test_04_sp_ice_cream_area_numerical")
        th = sp.Symbol('theta', positive=True, real=True)
        a  = sp.Symbol('a', positive=True, real=True)
        
        expr = sp_ice_cream_area(th, a)
        f_np = sp_to_np(expr)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] f_np type =", type(f_np))
        
        print("[CHECK] NumPy-converted function is callable ...")
        self.assertTrue(callable(f_np))
        print("[PASS] NumPy-converted function is callable")
        
        test_cases = [
            (1.0, 0.1),
            (2.0, 0.2),
            (3.5, 0.5),
            (10.0, 1.0),
        ]
        
        for aval, thval in test_cases:
            print(f"[INFO] Testing a={aval}, theta={thval}")
            
            # sp_to_np sorts free symbols by name, so args are (a, theta)
            got = float(f_np(aval, thval))
            
            # numerical reference computed from definition:
            # I(theta) = (pi/2)*(b(theta)/2)^2
            b_val = 2.0 * aval * np.sin(thval / 2.0)
            ref = (np.pi / 2.0) * (b_val / 2.0) ** 2
            
            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")
            
            # We use assertAlmostEqual() because floating point computations
            # introduce rounding errors even when the math is correct.
            self.assertAlmostEqual(got, ref, places=12)
            
        print("[SUCCESS] test_04_sp_ice_cream_area_numerical PASSED!!!")

    def test_05_sp_cone_area_structural(self):
        print("\n[Test] test_05_sp_cone_area_structural")
        th = sp.Symbol('theta', positive=True, real=True)
        a  = sp.Symbol('a', positive=True, real=True)

        expr = sp_cone_area(th, a)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        print("[INFO] free symbols:", expr.free_symbols)
        
        # --- Must depend on theta and a ---
        print("[CHECK] expr depends on theta ...")
        self.assertTrue(expr.has(th))
        print("[PASS] expr depends on theta")
        
        print("[CHECK] expr depends on a ...")
        self.assertTrue(expr.has(a))
        print("[PASS] expr depends on a")
        
        # ----------------------------------------------------------
        # IMPORTANT SymPy Note for you to remember:
        #
        # SymPy often rewrites sqrt(x) as x**(1/2).
        # That is, sqrt(x) is represented internally as a Pow object:
        #
        #     sqrt(x)  <=>  x**(1/2)
        #
        # Therefore, checking for "sqrt" directly may not always work.
        # A more robust structural check is to find Pow terms whose
        # exponent is Rational(1,2).
        # ----------------------------------------------------------
        pow_terms = list(expr.atoms(sp.Pow))
        sqrt_like_terms = [p for p in pow_terms if p.exp == sp.Rational(1, 2)]
        
        print("[INFO] Pow terms found:", pow_terms)
        print("[INFO] sqrt-like terms (Pow with exp=1/2):", sqrt_like_terms)
        
        print("[CHECK] at least 1 sqrt-like Pow term exists ...")
        self.assertGreaterEqual(len(sqrt_like_terms), 1)
        print("[PASS] at least 1 sqrt-like Pow term exists")
        
        # --- Must contain sin term(s) ---
        sin_terms = list(expr.atoms(sp.sin))
        print("[INFO] sin terms found:", sin_terms)
        
        print("[CHECK] at least 1 sin term exists ...")
        self.assertGreaterEqual(len(sin_terms), 1)
        print("[PASS] at least 1 sin term exists")
        
        # --- Must contain sin(theta/2) ---
        found_sin_theta_over_2 = False
        for s in sin_terms:
            if sp.simplify(s.args[0] - th/2) == 0:
                found_sin_theta_over_2 = True
                break
            
        print("[CHECK] sin argument includes theta/2 ...")
        self.assertTrue(found_sin_theta_over_2)
        print("[PASS] sin argument includes theta/2")

        print("[SUCCESS] test_05_sp_cone_area_structural PASSED!!!")

    def test_06_sp_cone_area_numerical(self):
        print("\n[Test] test_06_sp_cone_area_numerical")
        th = sp.Symbol('theta', positive=True, real=True)
        a  = sp.Symbol('a', positive=True, real=True)
        
        expr = sp_cone_area(th, a)
        f_np = sp_to_np(expr)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] f_np type =", type(f_np))
        
        print("[CHECK] NumPy-converted function is callable ...")
        self.assertTrue(callable(f_np))
        print("[PASS] NumPy-converted function is callable")
        
        # (a, theta) numerical test cases.
        # theta is positive and not too large to avoid numerical edge issues.
        test_cases = [
            (1.0, 0.1),
            (2.0, 0.2),
            (3.5, 0.5),
            (10.0, 1.0),
        ]
        
        for aval, thval in test_cases:
            print(f"[INFO] Testing a={aval}, theta={thval}")
            
            # sp_to_np sorts free symbols by name, so args are (a, theta)
            got = float(f_np(aval, thval))
            
            # Numerical reference computed directly from the definition:
            # C(theta) = (b/4) * sqrt(4*a^2 - b^2)
            # where b(theta) = 2*a*sin(theta/2)
            b_val = 2.0 * aval * np.sin(thval / 2.0)
            ref = (b_val / 4.0) * np.sqrt(4.0 * aval * aval - b_val * b_val)

            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")

            # We use assertAlmostEqual() because floating point computations
            # introduce rounding errors even when the math is correct.
            self.assertAlmostEqual(got, ref, places=12)

        print("[SUCCESS] test_06_sp_cone_area_numerical PASSED!!!")

    def test_07_sp_ice_cream_rat_structural(self):
        print("\n[Test] test_07_sp_ice_cream_rat_structural")
        th = sp.Symbol('theta', positive=True, real=True)
        a  = sp.Symbol('a', positive=True, real=True)

        expr = sp_ice_cream_rat(th, a)

        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        print("[INFO] free symbols:", expr.free_symbols)
        
        # --- Must depend on theta and a ---
        print("[CHECK] expr depends on theta ...")
        self.assertTrue(expr.has(th))
        print("[PASS] expr depends on theta")

        print("[CHECK] expr depends on a ...")
        self.assertTrue(expr.has(a))
        print("[PASS] expr depends on a")
        
        # --- Must contain pi (comes from ice cream area) ---
        print("[CHECK] expr contains pi ...")
        self.assertTrue(expr.has(sp.pi))
        print("[PASS] expr contains pi")

        # --- Must contain at least one sin(theta/2) ---
        sin_terms = list(expr.atoms(sp.sin))
        print("[INFO] sin terms found:", sin_terms)

        print("[CHECK] at least 1 sin term exists ...")
        self.assertGreaterEqual(len(sin_terms), 1)
        print("[PASS] at least 1 sin term exists")

        found_sin_theta_over_2 = False
        for s in sin_terms:
            if sp.simplify(s.args[0] - th/2) == 0:
                found_sin_theta_over_2 = True
                break

        print("[CHECK] sin argument includes theta/2 ...")
        self.assertTrue(found_sin_theta_over_2)
        print("[PASS] sin argument includes theta/2")

        # --- Must contain a division structure ---
        # SymPy represents division as a Mul with a Pow(..., -1) factor.
        pow_terms = list(expr.atoms(sp.Pow))
        inv_terms = [p for p in pow_terms if p.exp.is_negative]

        print("[INFO] Pow terms found:", pow_terms)
        print("[INFO] inverse-like Pow terms (exp < 0):", inv_terms)

        print("[CHECK] at least 1 inverse-like Pow term exists ...")
        self.assertGreaterEqual(len(inv_terms), 1)
        print("[PASS] at least 1 inverse-like Pow term exists")

        print("[SUCCESS] test_07_sp_ice_cream_rat_structural PASSED!!!")

    def test_08_sp_ice_cream_rat_numerical(self):
        print("\n[Test] test_08_sp_ice_cream_rat_numerical")
        th = sp.Symbol('theta', positive=True, real=True)
        a  = sp.Symbol('a', positive=True, real=True)

        expr = sp_ice_cream_rat(th, a)
        f_np = sp_to_np(expr)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] f_np type =", type(f_np))

        print("[CHECK] NumPy-converted function is callable ...")
        self.assertTrue(callable(f_np))
        print("[PASS] NumPy-converted function is callable")

        test_cases = [
            (1.0, 0.1),
            (2.0, 0.2),
            (3.5, 0.5),
            (10.0, 1.0),
        ]

        for aval, thval in test_cases:
            print(f"[INFO] Testing a={aval}, theta={thval}")

            # sp_to_np sorts free symbols by name, so args are (a, theta)
            got = float(f_np(aval, thval))

            # Numerical reference computed from definition:
            # Rat(theta) = I(theta) / C(theta)
            #
            # I(theta) = (pi/2)*(b(theta)/2)^2
            # C(theta) = (b(theta)/4)*sqrt(4*a^2 - b(theta)^2)
            # b(theta) = 2*a*sin(theta/2)
            b_val = 2.0 * aval * np.sin(thval / 2.0)

            I_ref = (np.pi / 2.0) * (b_val / 2.0) ** 2
            C_ref = (b_val / 4.0) * np.sqrt(4.0 * aval * aval - b_val * b_val)

            ref = I_ref / C_ref

            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")

            # We use assertAlmostEqual() because floating point computations
            # introduce rounding errors even when the math is correct.
            self.assertAlmostEqual(got, ref, places=12)

        print("[SUCCESS] test_08_sp_ice_cream_rat_numerical PASSED!!!")

    def test_09_sp_ice_cream_rat_limit_structural(self):
        print("\n[Test] test_09_sp_ice_cream_rat_limit_structural")
        th = sp.Symbol('theta', positive=True, real=True)
        a  = sp.Symbol('a', positive=True, real=True)
        
        expr = sp_ice_cream_rat_limit(th, a)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        
        # For this problem, the limit should be a SymPy expression
        # that evaluates to 0 exactly.
        print("[CHECK] limit expression equals 0 ...")
        self.assertEqual(expr, 0)
        print("[PASS] limit expression equals 0")
        
        print("[SUCCESS] test_09_sp_ice_cream_rat_limit_structural PASSED!!!")

    def test_10_sp_ice_cream_rat_limit_numerical(self):
        print("\n[Test] test_10_sp_ice_cream_rat_limit_numerical")
        th = sp.Symbol('theta', positive=True, real=True)
        a  = sp.Symbol('a', positive=True, real=True)

        # ----------------------------------------------------------
        # IMPORTANT:
        #
        # Sometimes SymPy expressions look complicated, and it helps to call
        # sp.simplify() before taking the limit. In many cases, SymPy can still
        # compute the correct limit without simplify().
        #
        # In this unit test, we compute the limit in TWO ways:
        #
        #   (1) limit of the raw ratio expression
        #   (2) limit of the simplified ratio expression
        #
        # Both limits should be 0.
        # ----------------------------------------------------------

        rat_expr = sp_ice_cream_rat(th, a)
        print("[INFO] rat_expr =", rat_expr)

        L_raw = sp.limit(rat_expr, th, 0, dir='+')
        print("[INFO] L_raw =", L_raw)

        simp_rat_expr = sp.simplify(rat_expr)
        print("[INFO] simplify(rat_expr) =", simp_rat_expr)

        L_simp = sp.limit(simp_rat_expr, th, 0, dir='+')
        print("[INFO] L_simp =", L_simp)

        print("[CHECK] L_raw equals 0 ...")
        self.assertEqual(L_raw, 0)
        print("[PASS] L_raw equals 0")

        print("[CHECK] L_simp equals 0 ...")
        self.assertEqual(L_simp, 0)
        print("[PASS] L_simp equals 0")
        
        print("[SUCCESS] test_10_sp_ice_cream_rat_limit_numerical PASSED!!!")
        
if __name__ == "__main__":
    print("\nRunning CS3430 S26 HW2 Problem 1 unit tests...\n")
    unittest.main(verbosity=2)
    pass

