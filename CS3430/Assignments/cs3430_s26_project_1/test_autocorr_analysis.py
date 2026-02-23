"""
===========================================================
test_autocorr_analysis.py

Main compiler of hive-specific autocorrelation analyses 
for CS3430 S26 Project 1.
-- bugs to vladimir kulyukin in canvas.

This file does autocorrelation testing for hive weight
and temp series. The directory csv is assumed to 
be in the same directory with this file. I ran
one test class at a time while commenting out
the other ones.

NO # YOUR CODE HERE IN THIS FILE. 

Copyright (C) Vladimir Kulyukin. All rights reserved.
For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
==============================================================
"""

import unittest
import os

from autocorr_analysis import run_autocorr_analysis

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(BASE_DIR, "csv")

# ==========================================================
# Hive 83
# ==========================================================

'''
YOUR REPORT FOR HIVE 83

'''


class TestHive83Autocorr(unittest.TestCase):

    def test_hive_83(self):
        print("\n[Test] Running autocorrelation analysis for Hive 83")
        csv_path = os.path.join(BASE_PATH, "hive_83_data.csv")
        run_autocorr_analysis(csv_path)

# ==========================================================
# Hive 84
# ==========================================================

'''
YOUR REPORT FOR HIVE 84

'''

class TestHive84Autocorr(unittest.TestCase):

    def test_hive_84(self):
        print("\n[Test] Running autocorrelation analysis for Hive 84")
        csv_path = os.path.join(BASE_PATH, "hive_84_data.csv")
        run_autocorr_analysis(csv_path)

'''
YOUR SUMMARY REPORT FOR HIVES: 83, 84, 94, 97, 104

'''

# ==========================================================
# Hive 94
# ==========================================================

'''
YOUR REPORT FOR HIVE 94 HERE.

'''

class TestHive94Autocorr(unittest.TestCase):

    def test_hive_94(self):
        print("\n[Test] Running autocorrelation analysis for Hive 94")
        csv_path = os.path.join(BASE_PATH, "hive_94_data.csv")
        run_autocorr_analysis(csv_path)

# ==========================================================
# Hive 97
# ==========================================================

'''
YOUR REPORT FOR HIVE 97

'''

class TestHive97Autocorr(unittest.TestCase):

    def test_hive_97(self):
        print("\n[Test] Running autocorrelation analysis for Hive 97")
        csv_path = os.path.join(BASE_PATH, "hive_97_data.csv")
        run_autocorr_analysis(csv_path)


# ==========================================================
# Hive 104
# ==========================================================

'''
YOUR REPORT FOR HIVE 104 HERE.

'''

class TestHive104Autocorr(unittest.TestCase):

    def test_hive_104(self):
        print("\n[Test] Running autocorrelation analysis for Hive 104")
        csv_path = os.path.join(BASE_PATH, "hive_104_data.csv")
        run_autocorr_analysis(csv_path)


if __name__ == "__main__":
    unittest.main()
