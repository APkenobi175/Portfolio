# data_processing.py
# 
# This file loads temperature and weight time series from the files in csv/.
# It also implements three types of detrending (raw, global, diurnal).
# -- bugs to vladimir kulyukin in canvas.
# 
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
# Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
# ========================================================================================

import csv
from datetime import datetime
from typing import Dict, Tuple, Sequence
import numpy as np
import math
from scipy.stats import norm

def load_series(csv_path: str) -> Dict[Tuple[int, str], dict]:
    """
    Load hive temperature and weight data from a CSV file.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file containing the hive data.

    Returns
    -------
    data : dict
        Dictionary keyed by (hive:int, direction:str).

        For each key, the value is a dictionary with:
            {
                "temp":   (t_temp, y_temp),
                "weight": (t_weight, y_weight)
            }

        where:
            - t_* : list of datatime time stamps
            - y_* : np.ndarray of float measurements

    Notes
    -----
    - Missing temperature or weight values are skipped independently.
    - No interpolation or imputation is performed.
    - Time is encoded as datetime timestamps.
    """

    # Temporary storage structure before NumPy conversion
    raw_data = {}

    #hive,direction,month,dayofmonth,year,hourofday,temp,weight    
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header row
        #print('skipping {}'.format(header))

        for row in reader:
            if not row or len(row) < 8:
                #print('skipping {}'.format(row))
                continue  # Skip malformed rows

            #print('row = {}'.format(row))
            hive = int(row[0])
            #print('hive = {}'.format(hive))
            direction = row[1]
            #print('direction = {}'.format(direction))

            month = int(row[2])
            #print('month = {}'.format(month))
            day   = int(row[3])
            #print('day = {}'.format(day))
            year  = int(row[4])
            #print('year = {}'.format(year))
            hour  = int(row[5])
            #print('hour = {}'.format(hour))

            temp_str   = row[6].strip()
            #print('temp_str = {}'.format(temp_str))
            weight_str = row[7].strip()
            #print('weight_str = {}'.format(weight_str))

            # Construct datetime object
            timestamp = datetime(year, month, day, hour)
            #print('timestamp = {}'.format(timestamp))

            key = (hive, direction)
            #print('key = {}'.format(key))

            if key not in raw_data:
                raw_data[key] = {
                    "temp": [],
                    "weight": []
                }

            # -----------------------------
            # Append temperature if present
            # -----------------------------
            if temp_str != "":
                temp_val = float(temp_str)
                raw_data[key]["temp"].append((timestamp, temp_val))
                #print("raw_data[{}][temp] = {}".format(key, raw_data[key]["temp"]))

            # -----------------------------
            # Append weight if present
            # -----------------------------
            if weight_str != "":
                weight_val = float(weight_str)
                raw_data[key]["weight"].append((timestamp, weight_val))
                #print("raw_data[{}][weight] = {}".format(key, raw_data[key]["weight"]))

    # ---------------------------------------------
    # Convert lists to sorted NumPy array outputs
    # ---------------------------------------------
    data = {}

    for key, series in raw_data.items():
        data[key] = {}

        for var_name in ["temp", "weight"]:
            entries = series[var_name]
            #print('entries = {}'.format(entries))

            if len(entries) == 0:
                # Return empty arrays if no data
                data[key][var_name] = (
                    [],
                    np.array([], dtype=float)
                )
                continue

            # Sort entries by timestamp
            entries.sort(key=lambda x: x[0])

            # Extract components
            timestamps = [e[0] for e in entries]
            values     = np.array([e[1] for e in entries], dtype=float)

            data[key][var_name] = (timestamps, values)
    return data

def detrend_global(y: np.ndarray) -> np.ndarray:
    """
    Remove global mean from a 1D numerical sequence.

    Parameters
    ----------
    y : np.ndarray
        1D array of float values.

    Returns
    -------
    y0 : np.ndarray
        Detrended sequence with mean removed.

    Notes
    -----
    - Does not modify input array in place.
    - If input is empty, returns empty array.
    """

    if y.size == 0:
        return np.array([], dtype=float)

    mean_value = np.mean(y)

    return y - mean_value


def detrend_diurnal_hourly_helper(y: np.ndarray, hour_of_day: np.ndarray) -> np.ndarray:
    """
    Remove diurnal (hour-of-day) mean pattern from a sequence.

    Parameters
    ----------
    y : np.ndarray
        1D array of float values.
    hour_of_day : np.ndarray
        1D array of integers in [0, 23] indicating hour.

    Returns
    -------
    y1 : np.ndarray
        Detrended sequence with hourly means removed.

    Notes
    -----
    - Does not modify input arrays.
    - Requires len(y) == len(hour_of_day).
    """

    if y.size == 0:
        return np.array([], dtype=float)

    if len(y) != len(hour_of_day):
        raise ValueError("y and hour_of_day must have same length.")

    if np.any((hour_of_day < 0) | (hour_of_day > 23)):
        raise ValueError("hour_of_day values must be between 0 and 23.")

    # Compute hourly means
    hourly_means = {}

    for h in np.unique(hour_of_day):
        mask = (hour_of_day == h)
        hourly_means[h] = np.mean(y[mask])

    # Subtract hourly means
    y1 = np.empty_like(y, dtype=float)

    for i in range(len(y)):
        y1[i] = y[i] - hourly_means[hour_of_day[i]]

    return y1

def detrend_diurnal(timestamps: list, y: np.ndarray) -> np.ndarray:
    """
    Remove diurnal (hour-of-day) mean pattern using datetime timestamps.

    Parameters
    ----------
    timestamps : list of datetime
        Timestamps corresponding to each observation.
    y : np.ndarray
        1D array of float values.

    Returns
    -------
    y1 : np.ndarray
        Detrended sequence with hourly means removed.

    Notes
    -----
    - Requires len(timestamps) == len(y).
    - Extracts hour-of-day from timestamps.
    - Delegates computation to detrend_diurnal_hourly_helper().
    """

    if y.size == 0:
        return np.array([], dtype=float)

    if len(timestamps) != len(y):
        raise ValueError("timestamps and y must have same length.")

    # Extract hour-of-day from datetime objects
    hour_of_day = np.array([ts.hour for ts in timestamps], dtype=int)

    return detrend_diurnal_hourly_helper(y, hour_of_day)


def autocorrelation(x: np.ndarray, lag: int) -> float:
    """
    Compute sample autocorrelation at a given lag.

    Parameters
    ----------
    x : array-like of float
        Numerical sequence.
    lag : int
        Lag at which to compute autocorrelation.

    Returns
    -------
    rho : float
        Sample autocorrelation coefficient.
    """

    x = np.asarray(x, dtype=float)
    n = x.size

    if lag <= 0 or lag >= n:
        raise ValueError("Lag must be between 1 and len(x)-1.")

    ### 1) Compute the mean of x and save it in the variable mean.
    ### You can use np.mean(sequence) here.
    mean = np.mean(x)


    ### 2) Compute the numerator of rho(k), where k = lag.
    ### You can use np.sum here along with the following
    ### NumPy array shortcut inside np.sum: (x[:n - lag] - mean) * (x[lag:] - mean).
    ### Save your computation in the variable num.

    num = np.sum((x[:n - lag] - mean) * (x[lag:] - mean))

    ### 3) Compute the denominator of rho(k) and save it in the
    ### variable den. Again, a useful NumPy shortcut here is to apply
    ### np.sum to (x - mean) ** 2.
    den = np.sum((x - mean) ** 2)

    if den == 0:
        raise ValueError("Variance is zero; autocorrelation undefined.")

    ### 4) Return rho(k).
    return num / den

def autocorrelation_test(x: np.ndarray, lag: int) -> tuple[float, float]:
    """
    Perform a hypothesis test for zero autocorrelation at a given lag.

    Parameters
    ----------
    x : array-like of float
        Numerical sequence.
    lag : int
        Lag at which to test autocorrelation.

    Returns
    -------
    z_stat : float
        Normalized test statistic.
    p_value : float
        Two-sided p-value.
    """

    x = np.asarray(x, dtype=float)
    n = x.size

    ### 1) Compute rho(k = lag).
    rho = autocorrelation(x, lag)

    ### 2) Do asymptotic normal approximation

    ### 2.1) Compute the z statistic and save
    ### it in the variable z. Remember that
    ### the z statistic is sqrt(n) * rho.
    ### You can use math.sqrt here.

    z = math.sqrt(n) * rho
    
    ### 2.2) Compute the p-value of the z statistic
    ### and save in the variable p_value. Remember
    ### that we need to compute both tails of
    ### normal distribution of |z|. This can be
    ### done by doubling the value of the survival function
    ### on |z|, i.e., 2 * norm.sf(abs(z))

    p_value = 2 * norm.sf(abs(z))

    ### 3) Return the z statistic and its p-value.
    return z, p_value
