#############################################################
# cs3430_s26_hw_2_prob_2_uts.py
# unit tests for CS3430 S26 HW2 Prob 2
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

from cs3430_s26_hw_2_prob_2 import sp_to_np, sp_laminar_velocity, sp_avg_rate_of_change
from cs3430_s26_hw_2_prob_2 import sp_velocity_gradient, sp_velocity_gradient_closed_form
from cs3430_s26_hw_2_prob_2 import sp_flow_rate_Q

class cs3430_s26_hw_2_prob_2_uts(unittest.TestCase):
    """
    Unit tests for Problem 2: Law of Laminar Flow
    """
    def test_01_sp_laminar_velocity_structural(self):
        print("\n[Test] test_01_sp_laminar_velocity_structural")

        r   = sp.Symbol('r', real=True)
        R   = sp.Symbol('R', positive=True, real=True)
        P   = sp.Symbol('P', positive=True, real=True)
        eta = sp.Symbol('eta', positive=True, real=True)
        l   = sp.Symbol('l', positive=True, real=True)
        
        expr = sp_laminar_velocity(r, R, P, eta, l)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        print("[INFO] free symbols:", expr.free_symbols)
        
        print("[CHECK] expr is a SymPy expression (sp.Expr) ...")
        self.assertIsInstance(expr, sp.Expr)
        print("[PASS] expr is a SymPy expression")
        
        print("[CHECK] expr depends on r ...")
        self.assertTrue(expr.has(r))
        print("[PASS] expr depends on r")
        
        print("[CHECK] expr depends on R ...")
        self.assertTrue(expr.has(R))
        print("[PASS] expr depends on R")
        
        print("[CHECK] expr depends on P ...")
        self.assertTrue(expr.has(P))
        print("[PASS] expr depends on P")
        
        print("[CHECK] expr depends on eta ...")
        self.assertTrue(expr.has(eta))
        print("[PASS] expr depends on eta")
        
        print("[CHECK] expr depends on l ...")
        self.assertTrue(expr.has(l))
        print("[PASS] expr depends on l")

        # Check that the expression contains a squared r term somewhere (r^2).
        pow_terms = list(expr.atoms(sp.Pow))
        print("[INFO] Pow terms found:", pow_terms)

        has_r_squared = False
        for p in pow_terms:
            if p.base == r and p.exp == 2:
                has_r_squared = True
                break

        print("[CHECK] expr contains r^2 ...")
        self.assertTrue(has_r_squared)
        print("[PASS] expr contains r^2")

        print("[SUCCESS] test_01_sp_laminar_velocity_structural PASSED!!!")

    def test_02_sp_laminar_velocity_numerical(self):
        print("\n[Test] test_02_sp_laminar_velocity_numerical")

        r   = sp.Symbol('r', real=True)
        R   = sp.Symbol('R', positive=True, real=True)
        P   = sp.Symbol('P', positive=True, real=True)
        eta = sp.Symbol('eta', positive=True, real=True)
        l   = sp.Symbol('l', positive=True, real=True)
        
        expr = sp_laminar_velocity(r, R, P, eta, l)
        f_np = sp_to_np(expr)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] f_np type =", type(f_np))
        
        print("[CHECK] NumPy-converted function is callable ...")
        self.assertTrue(callable(f_np))
        print("[PASS] NumPy-converted function is callable")
        
        # Test cases: (r, R, P, eta, l)
        test_cases = [
            (0.0, 2.0, 100.0, 4.0, 10.0),
            (0.5, 2.0, 100.0, 4.0, 10.0),
            (1.0, 2.0, 100.0, 4.0, 10.0),
            (2.0, 2.0, 100.0, 4.0, 10.0),  # at r=R, velocity should be 0
        ]
        
        for rval, Rval, Pval, etaval, lval in test_cases:
            print(f"[INFO] Testing r={rval}, R={Rval}, P={Pval}, eta={etaval}, l={lval}")

            # sp_to_np sorts free symbols by name:
            # expected order: (P, R, eta, l, r)
            got = float(f_np(Pval, Rval, etaval, lval, rval))

            ref = (Pval / (4.0 * etaval * lval)) * (Rval**2 - rval**2)

            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")

            # We use assertAlmostEqual() because floating point computations
            # introduce rounding errors even when the math is correct.
            self.assertAlmostEqual(got, ref, places=12)

            # Extra physical sanity check: v(R) should be 0
            print("[CHECK] velocity at r=R is approximately 0 ...")
            got_at_wall = float(f_np(100.0, 2.0, 4.0, 10.0, 2.0))
            print("       v(R) =", got_at_wall)
            self.assertAlmostEqual(got_at_wall, 0.0, places=12)
            print("[PASS] velocity at r=R is approximately 0")

        print("[SUCCESS] test_02_sp_laminar_velocity_numerical PASSED!!!")

    def test_03_sp_avg_rate_of_change_structural(self):
        print("\n[Test] test_03_sp_avg_rate_of_change_structural")

        r1  = sp.Symbol('r1', real=True)
        r2  = sp.Symbol('r2', real=True)
        R   = sp.Symbol('R', positive=True, real=True)
        P   = sp.Symbol('P', positive=True, real=True)
        eta = sp.Symbol('eta', positive=True, real=True)
        l   = sp.Symbol('l', positive=True, real=True)
        
        expr = sp_avg_rate_of_change(r1, r2, R, P, eta, l)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        print("[INFO] free symbols:", expr.free_symbols)
        
        print("[CHECK] expr is a SymPy expression (sp.Expr) ...")
        self.assertIsInstance(expr, sp.Expr)
        print("[PASS] expr is a SymPy expression")
        
        print("[CHECK] expr depends on r1 ...")
        self.assertTrue(expr.has(r1))
        print("[PASS] expr depends on r1")
        
        print("[CHECK] expr depends on r2 ...")
        self.assertTrue(expr.has(r2))
        print("[PASS] expr depends on r2")
        
        print("[CHECK] expr depends on R ...")
        self.assertTrue(expr.has(R))
        print("[PASS] expr depends on R")
        
        print("[CHECK] expr depends on P ...")
        self.assertTrue(expr.has(P))
        print("[PASS] expr depends on P")
        
        print("[CHECK] expr depends on eta ...")
        self.assertTrue(expr.has(eta))
        print("[PASS] expr depends on eta")
        
        print("[CHECK] expr depends on l ...")
        self.assertTrue(expr.has(l))
        print("[PASS] expr depends on l")
        
        # Since this is a difference quotient, the expression should contain (r2 - r1)
        # somewhere in the denominator. In SymPy, denominators often show up as Pow(...,-1).
        pow_terms = list(expr.atoms(sp.Pow))
        inv_terms = [p for p in pow_terms if p.exp.is_negative]
        
        print("[INFO] Pow terms found:", pow_terms)
        print("[INFO] inverse-like Pow terms (exp < 0):", inv_terms)
        
        print("[CHECK] at least 1 inverse-like Pow term exists ...")
        self.assertGreaterEqual(len(inv_terms), 1)
        print("[PASS] at least 1 inverse-like Pow term exists")
        
        # Light sanity check: expression should simplify to something finite
        # (we are not evaluating at r1=r2 here).
        simp_expr = sp.simplify(expr)
        print("[INFO] simplify(expr) =", simp_expr)

        print("[SUCCESS] test_03_sp_avg_rate_of_change_structural PASSED!!!")


    def test_04_sp_avg_rate_of_change_numerical(self):
        print("\n[Test] test_04_sp_avg_rate_of_change_numerical")

        r1  = sp.Symbol('r1', real=True)
        r2  = sp.Symbol('r2', real=True)
        R   = sp.Symbol('R', positive=True, real=True)
        P   = sp.Symbol('P', positive=True, real=True)
        eta = sp.Symbol('eta', positive=True, real=True)
        l   = sp.Symbol('l', positive=True, real=True)
        
        expr = sp_avg_rate_of_change(r1, r2, R, P, eta, l)
        f_np = sp_to_np(expr)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] f_np type =", type(f_np))
        
        print("[CHECK] NumPy-converted function is callable ...")
        self.assertTrue(callable(f_np))
        print("[PASS] NumPy-converted function is callable")
        
        # Test cases: (r1, r2, R, P, eta, l)
        # We avoid r1==r2 to prevent division by zero.
        test_cases = [
            (0.0, 0.5, 2.0, 100.0, 4.0, 10.0),
            (0.5, 1.0, 2.0, 100.0, 4.0, 10.0),
            (0.0, 1.0, 2.0, 100.0, 4.0, 10.0),
            (1.0, 2.0, 2.0, 100.0, 4.0, 10.0),
        ]
        
        for r1val, r2val, Rval, Pval, etaval, lval in test_cases:
            print(f"[INFO] Testing r1={r1val}, r2={r2val}, R={Rval}, P={Pval}, eta={etaval}, l={lval}")
            
            # sp_to_np sorts free symbols by name:
            # expected order: (P, R, eta, l, r1, r2)
            got = float(f_np(Pval, Rval, etaval, lval, r1val, r2val))
            
            # Reference computed directly from definition:
            def v(rr):
                return (Pval / (4.0 * etaval * lval)) * (Rval**2 - rr**2)

            ref = (v(r2val) - v(r1val)) / (r2val - r1val)

            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")

            self.assertAlmostEqual(got, ref, places=12)
            
        print("[SUCCESS] test_04_sp_avg_rate_of_change_numerical PASSED!!!")

    def test_05_sp_velocity_gradient_structural(self):
        print("\n[Test] test_05_sp_velocity_gradient_structural")

        r   = sp.Symbol('r', real=True)
        R   = sp.Symbol('R', positive=True, real=True)
        P   = sp.Symbol('P', positive=True, real=True)
        eta = sp.Symbol('eta', positive=True, real=True)
        l   = sp.Symbol('l', positive=True, real=True)
        
        expr = sp_velocity_gradient(r, R, P, eta, l)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        print("[INFO] free symbols:", expr.free_symbols)
        
        print("[CHECK] expr is a SymPy expression (sp.Expr) ...")
        self.assertIsInstance(expr, sp.Expr)
        print("[PASS] expr is a SymPy expression")
        
        # dv/dr should depend on r, P, eta, l
        print("[CHECK] expr depends on r ...")
        self.assertTrue(expr.has(r))
        print("[PASS] expr depends on r")
        
        print("[CHECK] expr depends on P ...")
        self.assertTrue(expr.has(P))
        print("[PASS] expr depends on P")
        
        print("[CHECK] expr depends on eta ...")
        self.assertTrue(expr.has(eta))
        print("[PASS] expr depends on eta")
        
        print("[CHECK] expr depends on l ...")
        self.assertTrue(expr.has(l))
        print("[PASS] expr depends on l")
        
        # After differentiation, dv/dr should NOT depend on R anymore
        print("[CHECK] expr does NOT depend on R ...")
        self.assertFalse(expr.has(R))
        print("[PASS] expr does NOT depend on R")
        
        # Gradient should be negative for positive r,P,eta,l (structure: contains a leading minus)
        # We do a light structural check: expr should simplify to something with r in numerator
        simp_expr = sp.simplify(expr)
        print("[INFO] simplify(expr) =", simp_expr)
        
        print("[CHECK] simplified expr contains r ...")
        self.assertTrue(simp_expr.has(r))
        print("[PASS] simplified expr contains r")
        
        print("[SUCCESS] test_05_sp_velocity_gradient_structural PASSED!!!")

    def test_06_sp_velocity_gradient_numerical(self):
        print("\n[Test] test_06_sp_velocity_gradient_numerical")

        r   = sp.Symbol('r', real=True)
        R   = sp.Symbol('R', positive=True, real=True)
        P   = sp.Symbol('P', positive=True, real=True)
        eta = sp.Symbol('eta', positive=True, real=True)
        l   = sp.Symbol('l', positive=True, real=True)
        
        expr = sp_velocity_gradient(r, R, P, eta, l)
        f_np = sp_to_np(expr)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] f_np type =", type(f_np))
        
        print("[CHECK] NumPy-converted function is callable ...")
        self.assertTrue(callable(f_np))
        print("[PASS] NumPy-converted function is callable")
        
        # Test cases: (r, R, P, eta, l)
        test_cases = [
            (0.0, 2.0, 100.0, 4.0, 10.0),
            (0.5, 2.0, 100.0, 4.0, 10.0),
            (1.0, 2.0, 100.0, 4.0, 10.0),
            (1.5, 2.0, 100.0, 4.0, 10.0),
        ]
        
        for rval, Rval, Pval, etaval, lval in test_cases:
            print(f"[INFO] Testing r={rval}, R={Rval}, P={Pval}, eta={etaval}, l={lval}")

            # sp_to_np sorts free symbols by name:
            # expected order: (P, eta, l, r)
            got = float(f_np(Pval, etaval, lval, rval))
            
            # Reference from calculus:
            # dv/dr = -(P*r)/(2*eta*l)
            ref = -(Pval * rval) / (2.0 * etaval * lval)
            
            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")

            self.assertAlmostEqual(got, ref, places=12)

        print("[SUCCESS] test_06_sp_velocity_gradient_numerical PASSED!!!")

    def test_07_sp_velocity_gradient_closed_form_structural(self):
        print("\n[Test] test_07_sp_velocity_gradient_closed_form_structural")

        r   = sp.Symbol('r', real=True)
        P   = sp.Symbol('P', positive=True, real=True)
        eta = sp.Symbol('eta', positive=True, real=True)
        l   = sp.Symbol('l', positive=True, real=True)
        
        expr = sp_velocity_gradient_closed_form(r, P, eta, l)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        print("[INFO] free symbols:", expr.free_symbols)
        
        print("[CHECK] expr is a SymPy expression (sp.Expr) ...")
        self.assertIsInstance(expr, sp.Expr)
        print("[PASS] expr is a SymPy expression")
        
        print("[CHECK] expr depends on r ...")
        self.assertTrue(expr.has(r))
        print("[PASS] expr depends on r")

        print("[CHECK] expr depends on P ...")
        self.assertTrue(expr.has(P))
        print("[PASS] expr depends on P")
        
        print("[CHECK] expr depends on eta ...")
        self.assertTrue(expr.has(eta))
        print("[PASS] expr depends on eta")
        
        print("[CHECK] expr depends on l ...")
        self.assertTrue(expr.has(l))
        print("[PASS] expr depends on l")
        
        # Structural check: expression should simplify to -(P*r)/(2*eta*l)
        simp_expr = sp.simplify(expr)
        print("[INFO] simplify(expr) =", simp_expr)
        
        print("[CHECK] simplified expr contains r ...")
        self.assertTrue(simp_expr.has(r))
        print("[PASS] simplified expr contains r")
        
        print("[SUCCESS] test_07_sp_velocity_gradient_closed_form_structural PASSED!!!")

    def test_08_sp_velocity_gradient_closed_form_numerical(self):
        print("\n[Test] test_08_sp_velocity_gradient_closed_form_numerical")

        r   = sp.Symbol('r', real=True)
        R   = sp.Symbol('R', positive=True, real=True)
        P   = sp.Symbol('P', positive=True, real=True)
        eta = sp.Symbol('eta', positive=True, real=True)
        l   = sp.Symbol('l', positive=True, real=True)
        
        expr_closed = sp_velocity_gradient_closed_form(r, P, eta, l)
        f_closed_np = sp_to_np(expr_closed)
        
        expr_diff = sp_velocity_gradient(r, R, P, eta, l)
        f_diff_np = sp_to_np(expr_diff)
        
        print("[INFO] expr_closed =", expr_closed)
        print("[INFO] expr_diff   =", expr_diff)
        
        print("[CHECK] closed-form NumPy function is callable ...")
        self.assertTrue(callable(f_closed_np))
        print("[PASS] closed-form NumPy function is callable")
        
        print("[CHECK] diff-based NumPy function is callable ...")
        self.assertTrue(callable(f_diff_np))
        print("[PASS] diff-based NumPy function is callable")
        
        # Test cases: (r, R, P, eta, l)
        test_cases = [
            (0.0, 2.0, 100.0, 4.0, 10.0),
            (0.5, 2.0, 100.0, 4.0, 10.0),
            (1.0, 2.0, 100.0, 4.0, 10.0),
            (1.5, 2.0, 100.0, 4.0, 10.0),
        ]

        for rval, Rval, Pval, etaval, lval in test_cases:
            print(f"[INFO] Testing r={rval}, R={Rval}, P={Pval}, eta={etaval}, l={lval}")
            
            # closed-form order: (P, eta, l, r)
            got_closed = float(f_closed_np(Pval, etaval, lval, rval))
            
            # diff-based order: (P, eta, l, r)
            got_diff = float(f_diff_np(Pval, etaval, lval, rval))
            
            ref = -(Pval * rval) / (2.0 * etaval * lval)
            
            print(f"       got_closed = {got_closed:.16e}")
            print(f"       got_diff   = {got_diff:.16e}")
            print(f"       ref        = {ref:.16e}")
            
            self.assertAlmostEqual(got_closed, ref, places=12)
            self.assertAlmostEqual(got_diff, ref, places=12)
            self.assertAlmostEqual(got_closed, got_diff, places=12)

        print("[SUCCESS] test_08_sp_velocity_gradient_closed_form_numerical PASSED!!!")

    def test_09_sp_flow_rate_Q_structural(self):
        print("\n[Test] test_09_sp_flow_rate_Q_structural")

        R   = sp.Symbol('R', positive=True, real=True)
        P   = sp.Symbol('P', positive=True, real=True)
        eta = sp.Symbol('eta', positive=True, real=True)
        l   = sp.Symbol('l', positive=True, real=True)
        
        expr = sp_flow_rate_Q(R, P, eta, l)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] expr type =", type(expr))
        print("[INFO] free symbols:", expr.free_symbols)
        
        print("[CHECK] expr is a SymPy expression (sp.Expr) ...")
        self.assertIsInstance(expr, sp.Expr)
        print("[PASS] expr is a SymPy expression")
        
        print("[CHECK] expr depends on R ...")
        self.assertTrue(expr.has(R))
        print("[PASS] expr depends on R")
        
        print("[CHECK] expr depends on P ...")
        self.assertTrue(expr.has(P))
        print("[PASS] expr depends on P")
        
        print("[CHECK] expr depends on eta ...")
        self.assertTrue(expr.has(eta))
        print("[PASS] expr depends on eta")
        
        print("[CHECK] expr depends on l ...")
        self.assertTrue(expr.has(l))
        print("[PASS] expr depends on l")
        
        print("[CHECK] expr contains pi ...")
        self.assertTrue(expr.has(sp.pi))
        print("[PASS] expr contains pi")
        
        # Structural check: we want to see R^4 explicitly.
        pow_terms = list(expr.atoms(sp.Pow))
        print("[INFO] Pow terms found:", pow_terms)
        
        has_R_fourth = False
        for p in pow_terms:
            if p.base == R and p.exp == 4:
                has_R_fourth = True
                break

        print("[CHECK] expr contains R^4 ...")
        self.assertTrue(has_R_fourth)
        print("[PASS] expr contains R^4")

        print("[SUCCESS] test_09_sp_flow_rate_Q_structural PASSED!!!")

    # ------------------------------------------------------------------
    # EDUCATIONAL NOTE (NOT MEDICAL ADVICE!!!):
    #
    # In real cardiovascular physiology, reduced blood flow to heart muscle
    # can contribute to ischemia (insufficient oxygen delivery), chest pain
    # (angina), and serious cardiac risk.
    #
    # A bypass surgery is one type of clinical intervention that can be used
    # to route blood around a severely narrowed or blocked artery.
    #
    # This homework uses Poiseuille's law as a simplified *laminar-flow model*
    # to illustrate a major computational takeaway:
    #
    #     Q is proportional to R^4
    #
    # meaning that even a small decrease in vessel radius R can cause a very
    # large decrease in flow rate Q.
    #
    # We are NOT diagnosing anything here. We are learning how scientific
    # computing can turn a mathematical model into computed quantities
    # that support decisions or warnings in real applications.
    # ------------------------------------------------------------------
    def test_10_sp_flow_rate_Q_numerical(self):
        print("\n[Test] test_10_sp_flow_rate_Q_numerical")

        R   = sp.Symbol('R', positive=True, real=True)
        P   = sp.Symbol('P', positive=True, real=True)
        eta = sp.Symbol('eta', positive=True, real=True)
        l   = sp.Symbol('l', positive=True, real=True)

        expr = sp_flow_rate_Q(R, P, eta, l)
        f_np = sp_to_np(expr)
        
        print("[INFO] Returned expression:")
        print("       expr =", expr)
        print("[INFO] f_np type =", type(f_np))
        
        print("[CHECK] NumPy-converted function is callable ...")
        self.assertTrue(callable(f_np))
        print("[PASS] NumPy-converted function is callable")
        
        # Test cases: (R, P, eta, l)
        test_cases = [
            (1.0, 100.0, 4.0, 10.0),
            (2.0, 100.0, 4.0, 10.0),
            (1.5, 200.0, 3.0, 8.0),
            (0.5, 150.0, 5.0, 12.0),
        ]
        
        for Rval, Pval, etaval, lval in test_cases:
            print(f"[INFO] Testing R={Rval}, P={Pval}, eta={etaval}, l={lval}")

            # sp_to_np sorts free symbols by name:
            # expected order: (P, R, eta, l)
            got = float(f_np(Pval, Rval, etaval, lval))

            ref = (np.pi * Pval * (Rval**4)) / (8.0 * etaval * lval)

            print(f"       got = {got:.16e}")
            print(f"       ref = {ref:.16e}")

            self.assertAlmostEqual(got, ref, places=12)

        # ------------------------------------------------------------------
        # BYPASS MOTIVATION (EDUCATIONAL MODEL):
        #
        # If an artery radius shrinks due to plaque, Q can drop dramatically.
        # A drop in Q means less blood can pass through per unit time.
        #
        # In real life, of course, doctors use far more complex imaging, tests, and models.
        # But this simplified computation demonstrates why severe narrowing may
        # require interventions such as a bypass (routing flow around the blockage).
        #
        # The key SciComp insight is: radius matters enormously because Q ~ R^4.
        # ------------------------------------------------------------------
        print("[CHECK] Doubling R multiplies Q by ~16 ...")
        Q1 = float(f_np(100.0, 1.0, 4.0, 10.0))
        Q2 = float(f_np(100.0, 2.0, 4.0, 10.0))
        ratio = Q2 / Q1
        print("       Q(R=1) =", Q1)
        print("       Q(R=2) =", Q2)
        print("       Q(R=2)/Q(R=1) =", ratio)

        self.assertAlmostEqual(ratio, 16.0, places=12)
        print("[PASS] Doubling R multiplies Q by ~16")

        print("[SUCCESS] test_10_sp_flow_rate_Q_numerical PASSED!!!")

    
if __name__ == "__main__":
    print("\nRunning CS3430 S26 HW2 Problem 2 unit tests...\n")
    unittest.main(verbosity=2)
    pass

