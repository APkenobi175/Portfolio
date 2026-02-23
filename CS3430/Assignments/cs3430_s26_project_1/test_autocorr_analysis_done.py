'''
===========================================================
test_autocorr_analysis.py

Main compiler of hive-specific autocorrelation analyses 
for CS3430 S26 Project 1.
-- bugs to vladimir kulyukin in canvas.

This file does autocorrelation testing for hive weight
and temp series. The directory csv is assumed to 
be in the same directory with this file. I ran
one test class at a time while commenting out
the other ones. There are the tests I have run. See 
my reports in samle_reports.

NO # YOUR CODE HERE IN THIS FILE. 

Copyright (C) Vladimir Kulyukin. All rights reserved.
For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
==============================================================
'''

import unittest
import os

from autocorr_analysis import run_autocorr_analysis

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "csv")

# ==========================================================
# Hive 82 -- DONE
# ==========================================================

class TestHive82Autocorr(unittest.TestCase):

    def test_hive_82(self):
        print("\n[Test] Running autocorrelation analysis for Hive 82")
        csv_path = os.path.join(BASE_PATH, "hive_82_data.csv")
        run_autocorr_analysis(csv_path)

# ==========================================================
# Hive 87 -- DONE
# ==========================================================

class TestHive87Autocorr(unittest.TestCase):

    def test_hive_87(self):
        print("\n[Test] Running autocorrelation analysis for Hive 87")
        csv_path = os.path.join(BASE_PATH, "hive_87_data.csv")
        run_autocorr_analysis(csv_path)

# ==========================================================
# Hive 90 -- DONE
# ==========================================================

class TestHive90Autocorr(unittest.TestCase):

    def test_hive_90(self):
        print("\n[Test] Running autocorrelation analysis for Hive 90")
        csv_path = os.path.join(BASE_PATH, "hive_90_data.csv")
        run_autocorr_analysis(csv_path)

# ==========================================================
# Hive 99 -- DONE
# ==========================================================

class TestHive99Autocorr(unittest.TestCase):

    def test_hive_99(self):
        print("\n[Test] Running autocorrelation analysis for Hive 99")
        csv_path = os.path.join(BASE_PATH, "hive_99_data.csv")
        run_autocorr_analysis(csv_path)

# ==========================================================
# Hive 103 -- DONE
# ==========================================================

class TestHive103Autocorr(unittest.TestCase):

    def test_hive_103(self):
        print("\n[Test] Running autocorrelation analysis for Hive 103")
        csv_path = os.path.join(BASE_PATH, "hive_103_data.csv")
        run_autocorr_analysis(csv_path)

if __name__ == "__main__":
    unittest.main()
