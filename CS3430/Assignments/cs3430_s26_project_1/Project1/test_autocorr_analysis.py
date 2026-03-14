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

Hive 83: WEST

1) Is Lag 1 Near 1? If yes, why?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9909 |   0.0000 | False
        Variable: WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9995 |   0.0000 | False
    
    Yes, lag 1 is near 1 in both temperature and weight. rho(k) = 0.9995 for weight and 0.9909 for temperature.
    This is likely because temperature and weight change slowly over time, leading to
    high correlation between consecutive measurements.

2) Does Global Mean Removal Change Anything? Why?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9909 |   0.0000 | False
        1 | global     |   0.9909 |   0.0000 | False
        Variable: WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9995 |   0.0000 | False
        1 | global     |   0.9995 |   0.0000 | False

    No, global mean removal does not change the results. The results are the same between raw and 
    the gloval removal detrending method. Global detrending removes the overal mean from the data
    but does not affect the correlation structure of the data, which is why the autocorrelation results
    are the same.

3) Does Dirunal Removal Change Lags 2, 3, or 24?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        2 | raw        |   0.9708 |   0.0000 | False
        2 | diurnal    |   0.9752 |   0.0000 | False
        3 | raw        |   0.9432 |   0.0000 | False
        3 | diurnal    |   0.9525 |   0.0000 | False
       24 | raw        |   0.8978 |   0.0000 | False
       24 | diurnal    |   0.8945 |   0.0000 | False
       Variable : WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
       24 | raw        |   0.9804 |   0.0000 | False
       24 | diurnal    |   0.9804 |   0.0000 | False

    Yes, dirnal removal changes the results for lags 2, 3, and 24 slightly for temperature
    but not for weight. It increaes between 2 and 3 and then decreases for 24. Weight is completely
    unchanged by diurnal removal. This indicates that there was no meaningful shift in weight
    measured throughout the day, but there were slight shifts in temperature that were removed
    by dirunal removal. 

4) Does Detrending Change Rejection of H0?

    No, as seen in the test results, the P-value remains 0, this means the null hypothesis is rejected
    for all detrending methods and lags. This indicates that there is very strong evidence of
    autocorrelation in the data.

5) As a Cyber-Physical System, Is This Hive Compatible With Independence With and Without Detrending?

    No, because the null hypothesis of independence is rejected for all detrending methods and lags, this hive
    is not compatible with independence. The strong autocorrelation may indicate that the measurements
    are NOT independent over time. Possibly due to weight and temperature being influenced by
    the previous measurments, or by external factors that change slowly over time.

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

HIVE 84: WEST

1) Is Lag 1 Near 1? If yes, why?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9929 |   0.0000 | False
        Variable: WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9998 |   0.0000 | False
    
    Yes, lag 1 is near 1 in both temperature and weight. rho(k) = 0.9998 for weight and 0.9929 for temperature.
    This is likely because temperature and weight change slowly over time, leading to predictable 
    measurments that are highly correlated with the last measurment.

2) Does Global Mean Removal Change Anything? Why?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9929 |   0.0000 | False
        1 | global     |   0.9929 |   0.0000 | False
        Variable: WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9998 |   0.0000 | False
        1 | global     |   0.9998 |   0.0000 | False

    No, global mean removal does not change the results. The results are the same between raw and 
    the global removal detrending method. Just like for hive 83, global detrending removes the
    overal mean from the data but it does not affect the correlation structure of the data,
    which is why the autocorrelation results are the same.

3) Does Dirunal Removal Change Lags 2, 3, or 24?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        2 | raw        |   0.9837 |   0.0000 | False
        2 | diurnal    |   0.9843 |   0.0000 | False
        3 | raw        |   0.9744 |   0.0000 | False
        3 | diurnal    |   0.9756 |   0.0000 | False
       24 | raw        |   0.9213 |   0.0000 | False
       24 | diurnal    |   0.9211 |   0.0000 | False
       Variable : WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
       24 | raw        |   0.9930 |   0.0000 | False
       24 | diurnal    |   0.9930 |   0.0000 | False

    Yes, dirnal removal changes the results for lags 2, 3, and 24 slightly for temperature
    but not for weight. It increaes between 2 and 3 and then decreases for 24. Weight is completely
    unchanged by diurnal removal. This indicates that there was no meaningful shift in weight
    measured throughout the day, but there were slight shifts in temperature that were removed
    by dirunal removal. 

    The changes are very small, and not meaningful, but it does prove that the sun exists.

    It is important and interesting to note that the lags are higher here than for hive 83, though 
    both hives reject the null hypothesis every time. This is interesting to note because both hives
    face the same direction.


4) Does Detrending Change Rejection of H0?

    No, similar to hive 83's test results, hive 84's test results show  the P-value remains 0,
    this means the null hypothesis is rejected for all detrending methods and lags. This
    indicates that there is very strong evidence of autocorrelation in the data.

5) As a Cyber-Physical System, Is This Hive Compatible With Independence With and Without Detrending?

    No, because the null hypothesis of independence is rejected for all detrending methods and lags, this hive
    is not compatible with independence. This indicates, similar to hive 83, that the measurments
    are NOT independant over time, likely because of weight and temperature being influence by
    the previous measurments, or by external factors that change slowly over time. (the sun)

'''

class TestHive84Autocorr(unittest.TestCase):

    def test_hive_84(self):
        print("\n[Test] Running autocorrelation analysis for Hive 84")
        csv_path = os.path.join(BASE_PATH, "hive_84_data.csv")
        run_autocorr_analysis(csv_path)

# ==========================================================
# Hive 94
# ==========================================================

'''
YOUR REPORT FOR HIVE 94 HERE.

HIVE 94: SOUTH

1) Is Lag 1 Near 1? If yes, why?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9954 |   0.0000 | False
        Variable: WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9998 |   0.0000 | False
    
    Yes, lag 1 is near 1 in both temperature and weight. rho(k) = 0.9998 for weight and 0.9954 for temperature.
    This is likely because temperature and weight change slowly over time, leading to predictable 
    measurments that are highly correlated with the last measurment.

2) Does Global Mean Removal Change Anything? Why?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9954 |   0.0000 | False
        1 | global     |   0.9954 |   0.0000 | False
        Variable: WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9998 |   0.0000 | False
        1 | global     |   0.9998 |   0.0000 | False

    No, global mean removal does not change the results. The results are the same between raw and 
    the global removal detrending method. Just like for hive 83 and 84.

3) Does Dirunal Removal Change Lags 2, 3, or 24?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        2 | raw        |   0.9871 |   0.0000 | False
        2 | diurnal    |   0.9888 |   0.0000 | False
        3 | raw        |   0.9768 |   0.0000 | False
        3 | diurnal    |   0.9805 |   0.0000 | False
       24 | raw        |   0.9486 |   0.0000 | False
       24 | diurnal    |   0.9481 |   0.0000 | False
       Variable : WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
       24 | raw        |   0.9928 |   0.0000 | False
       24 | diurnal    |   0.9928 |   0.0000 | False

    Yes, dirnal removal changes the results for lags 2, 3, and 24 slightly for temperature
    but not for weight. Unlike the previous 2 hives, this one goes down consistently with each
    lag. Weight is completely unchanged by diurnal removal. This indicates that there was no
    meaningful shift in weight measured throughout the day, but there were slight shifts in
    temperature that were removed by dirunal removal. 

    It is important and interesting to note that the lags are higher here than for hive 83, though 
    all 3 hives reject the null hypothesis every time. The difference between hive 94 and the previous
    2 hives is that our rho(k) values decrease more consistently as lag increases, while the 
    previous 2 hives were less consistent. 

    Despite these differences, all 3 hives so far show strong evidence of autocorrelation, and
    the null hypothesis is rejected every time, so the differences in lags are negligible.


4) Does Detrending Change Rejection of H0?

    No, similar to hive 83 and 84's test results, hive 94's test results show  the P-value remains 0,
    this means the null hypothesis is rejected for all detrending methods and lags. This
    indicates that there is very strong evidence of autocorrelation in the data.

5) As a Cyber-Physical System, Is This Hive Compatible With Independence With and Without Detrending?

    No, because the null hypothesis of independence is rejected for all detrending methods and lags, this hive
    is not compatible with independence. This indicates, that the measurments are NOT independant
    over time, and may be influenced by the previous measurments, or by
    external factors like the sun.

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

HIVE 97: SOUTH

1) Is Lag 1 Near 1? If yes, why?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9969 |   0.0000 | False
        Variable: WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9998 |   0.0000 | False
    
    Yes, lag 1 is near 1 in both temperature and weight. rho(k) = 0.9998 for weight and 0.9969 for temperature.
    This is likely because temperature and weight change slowly over time, leading to predictable 
    measurments that are highly correlated with the last measurment.

2) Does Global Mean Removal Change Anything? Why?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9969 |   0.0000 | False
        1 | global     |   0.9969 |   0.0000 | False
        Variable: WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9998 |   0.0000 | False
        1 | global     |   0.9998 |   0.0000 | False

    No, global mean removal does not change the results. The results are the same between raw and 
    the global removal detrending method.

3) Does Dirunal Removal Change Lags 2, 3, or 24?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        2 | raw        |   0.9911 |   0.0000 | False
        2 | diurnal    |   0.9920 |   0.0000 | False
        3 | raw        |   0.9838 |   0.0000 | False
        3 | diurnal    |   0.9858 |   0.0000 | False
       24 | raw        |   0.9433 |   0.0000 | False
       24 | diurnal    |   0.9432 |   0.0000 | False
       Variable : WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
       24 | raw        |   0.9928 |   0.0000 | False
       24 | diurnal    |   0.9928 |   0.0000 | False

    Yes, dirnal removal changes the results for lags 2, 3, and 24 slightly for temperature
    but not for weight. Similar to hive 84, the rho(k) values go slightly higher with each
    Lag, but then decrease again at lag 24. However, these changes in values are very minor, 
    and the weight values are unchanged by diurnal removal. This indicates that there was no
    meaningful shift in weight measured throughout the day, but there were slight shifts in
    temperature that were removed by dirunal removal. 

    It is important to note that hive 84 and hive 97 have similar results, but they face different 
    directions. up to this point we have 2 hives facing west and 2 hives facing south,
    and the results are very simlar between the 4 hives

    Despite these differences, all 4 hives so far show strong evidence of autocorrelation, and
    the null hypothesis is rejected every time, so the differences in lags are negligible.


4) Does Detrending Change Rejection of H0?

    No, similar to the previous test results, hive 97's test results show  the P-value remains 0,
    this means the null hypothesis is rejected for all detrending methods and lags. This
    indicates that there is very strong evidence of autocorrelation in the data.

5) As a Cyber-Physical System, Is This Hive Compatible With Independence With and Without Detrending?

    No, because the null hypothesis of independence is rejected for all detrending methods and lags, this hive
    is not compatible with independence. This indicates, that the measurments are NOT independant
    over time, and may be influenced by the previous measurments, or by external factors like
    the sun, or temperatures at different times of the day.

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

HIVE 104: NORTH

1) Is Lag 1 Near 1? If yes, why?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9950 |   0.0000 | False
        Variable: WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9997 |   0.0000 | False
    
    Yes, lag 1 is near 1 in both temperature and weight. rho(k) = 0.9997 for weight and 0.9950 for temperature.
    This is likely because temperature and weight change slowly over time, leading to predictable 
    measurments that are highly correlated with the last measurment.

2) Does Global Mean Removal Change Anything? Why?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9950 |   0.0000 | False
        1 | global     |   0.9950 |   0.0000 | False
        Variable: WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        1 | raw        |   0.9997 |   0.0000 | False
        1 | global     |   0.9997 |   0.0000 | False

    No, global mean removal does not change the results. The results are the same between raw and 
    the global removal detrending method.

3) Does Dirunal Removal Change Lags 2, 3, or 24?

    Test results:
        Variable: TEMP
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
        2 | raw        |   0.9857 |   0.0000 | False
        2 | diurnal    |   0.9885 |   0.0000 | False
        3 | raw        |   0.9732 |   0.0000 | False
        3 | diurnal    |   0.9791 |   0.0000 | False
       24 | raw        |   0.9530 |   0.0000 | False
       24 | diurnal    |   0.9522 |   0.0000 | False
       Variable : WEIGHT
        Lag | Detrending |  rho(k)  |  p-value  | H0 Not Rejected
        ----------------------------------------------------------
       24 | raw        |   0.9897 |   0.0000 | False
       24 | diurnal    |   0.9897 |   0.0000 | False

    Yes, dirnal removal changes the results for lags 2, 3, and 24 slightly for temperature
    but not for weight. Similar to hive 94, this one goes down consistently with each
    lag. Which, is interesting to note because they face opposit direction. Weight is
    completely unchanged by diurnal removal. This indicates that there was no meaningful shift
    in weight measured throughout the day, but there were slight shifts in temperature that
    were removed by dirunal removal. 

    It is interesting to note that hive 94 and hive 104 have very similar results, but they face
    opposite directions.

    Despite these differences, all hives show strong evidence of autocorrelation, and
    the null hypothesis is rejected every time, so the differences in lags are negligible.


4) Does Detrending Change Rejection of H0?

    No, similar to the other hives, the P-value remains 0, this means the null hypothesis is
    rejected for all detrending methods and lags. This indicates that there is very strong
    evidence of autocorrelation in the data.

5) As a Cyber-Physical System, Is This Hive Compatible With Independence With and Without Detrending?

    No, because the null hypothesis of independence is rejected for all detrending methods and lags, this hive
    is not compatible with independence. This indicates, that the measurments are NOT independant
    over time.

'''

class TestHive104Autocorr(unittest.TestCase):

    def test_hive_104(self):
        print("\n[Test] Running autocorrelation analysis for Hive 104")
        csv_path = os.path.join(BASE_PATH, "hive_104_data.csv")
        run_autocorr_analysis(csv_path)


# ==========================================================
# SUMMARY REPORT FOR HIVES 83, 84, 94, 97, 104
# ==========================================================

'''
YOUR SUMMARY REPORT FOR HIVES: 83, 84, 94, 97, 104


I tested 5 hives:
    1. Hive 83: WEST
    2. Hive 84: WEST
    3. Hive 94: SOUTH
    4. Hive 97: SOUTH
    5. Hive 104: NORTH

5 Hives Statistics Summary:
    Variable: TEMPERATURE
        Results for Lag 1 (raw) from greatest to least:
            Hive 97 - South - 0.9969
            Hive 94 - South - 0.9954
            Hive 104 - North - 0.9950
            Hive 84 - West - 0.9929
            Hive 83 - West - 0.9909
        Results for Lag 24 (raw) from greatest to least:
            Hive 104 - North - 0.9530
            Hive 94 - South - 0.9486
            Hive 97 - South - 0.9433
            Hive 84 - West - 0.9213
            Hive 83 - West - 0.8978

        Results for Lag 1 (global) from greatest to least:
            Hive 97 - South - 0.9969
            Hive 94 - South - 0.9954
            Hive 104 - North - 0.9950
            Hive 84 - West - 0.9929
            Hive 83 - West - 0.9909

        Results for Lag 24 (global) from greatest to least:
            Hive 104 - North - 0.9530
            Hive 94 - South - 0.9486
            Hive 97 - South - 0.9433
            Hive 84 - West - 0.9213
            Hive 83 - West - 0.8978

        Results for Lag 1 (diurnal) from greatest to least:
            Hive 97 - South - 0.9971
            Hive 94 - South - 0.9959
            Hive 104 - North - 0.9957
            Hive 84 - West - 0.9931
            Hive 83 - West - 0.9920

        Results for Lag 24 (diurnal) from greatest to least:
            Hive 104 - North - 0.9522
            Hive 94 - South - 0.9481
            Hive 97 - South - 0.9432
            Hive 84 - West - 0.9211
            Hive 83 - West - 0.8945

    Variable: WEIGHT

        Results for Lag 1 (raw) from greatest to least:
            Hive 84 - West - 0.9998
            Hive 94 - South - 0.9998
            Hive 97 - South - 0.9998
            Hive 104 - North - 0.9997
            Hive 83 - West - 0.9995
        Results for Lag 24 (raw) from greatest to least:
            Hive 84 - West - 0.9930
            Hive 94 - South - 0.9928
            Hive 97 - South - 0.9928
            Hive 104 - North - 0.9897
            Hive 83 - West - 0.9804

        Results are identical for global, diurnal, and raw detrending methods for weight,
        with the same order of hives from greatest to least as raw detrending method.

1) Is Lag 1 Near 1? If yes, why?
    Yes, lag 1 is near 1 in both temperature and weight for all 5 hives.
    This is likely because temperature and weight change slowly over time,
    leading to predictable measurments that are highly correlated with the last measurment.

    It is interesting to note that the hives that face the same direction have a closer relationship
    than with hives that face different directions for Lag 1, but this relationship is not consistent
    for the weight variable. 

    Poor hive 83 has the lowest lag value for both temperature and weight no matter what.

2) Does Global Mean Removal Change Anything? Why?
    No, global mean removal does not change the results. The results are the same between raw and 
    the global removal detrending method for all 5 hives.

3) Does Dirunal Removal Change Lags 2, 3, or 24?
    Yes, dirunal removal changes the results for lags 2, 3, and 24 slightly for temperature but
    not for weight for all 5 hives. It is interesting to note that the changes are not consistent
    regardless of the direction the hive faces, and they are so minor that they are not meaningful,
    but it does "verify that the sun exists, which is reassuring" ...

4) Does Detrending Change Rejection of H0?
    No, for all 5 hives, the P-value remains 0 for all detrending methods and lags, this
    means the null hypothesis is rejected for all hives regardless of facing direction,
    detrending method, and lag.

5) As a Cyber-Physical System, Is This Hive Compatible With Independence With and Without Detrending?
    No, because the null hypothesis of independence is rejected for all detrending methods and
    lags. Having statistical independance would require that each lag's measurment is not influenced
    or correlated with the other lags' measurments. That is not the case for any of the 5 hives.


    
In Conclusion, all 5 hives show strong evidence of correlation because the null hypothesis of 
independance is rejected for all 5. This is regardless of the direction the hive faces,
the detrending method, and the lag. It is also important to note that the weight is always
more correlated than the temperature for all 5 hives.

This summary indicates that the way the hive faces has no meaningful impact on how the hive 
behaves.
'''


if __name__ == "__main__":
    unittest.main()
