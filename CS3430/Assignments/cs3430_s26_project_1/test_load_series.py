# test_load_series.py
#
# This file tests structural integrity of the data loaded from the files in csv/.
# It tests load_series, and then runs 10 hive-specific data integrity test classes
# on each .csv file.
# -- bugs to vladimir kulyukin in canvas.
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero, Chegg, GitHub, ChatGPT, Gemini,
# Co-Pilot, Claude, DeepSeek, public drives, any LLMs) without prior written permission.
# ========================================================================================

import unittest
import tempfile
import os
import numpy as np
import csv

from data_processing import load_series

SAMPLE_CSV = """hive,direction,month,dayofmonth,year,hourofday,temp,weight
103,East,11,26,2019,11,18.485,
103,East,11,26,2019,12,22.364,
103,East,11,26,2019,13,20.708,
103,East,11,26,2019,14,26.617,
103,East,11,26,2019,15,27.054,
103,East,12,3,2019,0,34.326,24.737904596666667
103,East,12,3,2019,1,34.1075,24.743724356666664
103,East,12,3,2019,2,34.326,24.7494713725
103,East,12,3,2019,3,34.357,24.75514564
103,East,12,3,2019,4,34.295,24.7622384725
"""

class TestLoadSeries(unittest.TestCase):
    """
    Unit tests for load_series().

    These tests verify:
    1. Correct key creation per (hive, direction).
    2. Proper handling of missing weight values.
    3. Correct NumPy output types.
    4. Chronological sorting of time stamps
    """

    def setUp(self):
        """Create a temporary CSV file for testing."""
        print("\n[Setup] Creating temporary CSV file for testing.")
        self.tmp = tempfile.NamedTemporaryFile(mode="w", delete=False)
        self.tmp.write(SAMPLE_CSV)
        self.tmp.close()

    def tearDown(self):
        """Remove temporary CSV file after tests."""
        print("[Teardown] Removing temporary CSV file.")
        os.unlink(self.tmp.name)

    # --------------------------------------------------

    def test_display_table(self):
        print("[Test] Display table...")
        data = load_series(self.tmp.name)
        print(data)

    def test_keys_created(self):
        """
        Verify that distinct (hive, direction) pairs
        produce distinct dictionary keys.
        """
        print("[Test] Checking key creation...")
        data = load_series(self.tmp.name)

        print("Keys found:", list(data.keys()))

        self.assertIn((103, "East"), data)
        self.assertEqual(len(data), 1)

    def test_missing_weight(self):
        """
        Verify that missing weight entries are skipped
        while temperature entries are preserved.
        """
        print("[Test] Checking handling of missing weight values...")
        data = load_series(self.tmp.name)

        t_temp, y_temp = data[(103, "East")]["temp"]
        t_weight, y_weight = data[(103, "East")]["weight"]

        print("Temperature length:", len(y_temp))
        print("Weight length:", len(y_weight))

        self.assertEqual(len(y_temp), 10)
        self.assertEqual(len(y_weight), 5)

    def test_timestamps_and_values(self):
        """
        Verify that returned time and measurement
        arrays are List (timestamps) and NumPy (temperature and weight).
        """
        print("[Test] Checking Timestamps and NumPy array types...")
        data = load_series(self.tmp.name)

        t_temp, y_temp = data[(103, "East")]["temp"]

        print("Type of time array:",  type(t_temp))
        print("Type of value array:", type(y_temp))

        self.assertIsInstance(t_temp, list)
        self.assertIsInstance(y_temp, np.ndarray)

    def test_chronological_sorting(self):
        """
        Verify that timestamps are sorted.
        """
        data = load_series(self.tmp.name)
        t_temp, _ = data[(103, "East")]["temp"]
        self.assertEqual(t_temp, sorted(t_temp))


class TestHive82Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_82_data.csv

    This test enforces the following invariants:

    1. The file must contain exactly 6770 non-empty data rows
       (excluding the header line).
    2. Every data row must contain exactly 8 comma-separated fields.
    3. The hive column must be 82 in every row.
    4. The direction column must be "East" in every row.
    5. The temperature field must be non-empty in every row.
    6. The weight field may be empty or numeric (no constraint on count).

    The test fails immediately on the first violation.
    """

    def test_hive_82_csv_structure(self):
        print("[Test] Hive 82 CSV consistency check...")

        path = "csv/hive_82_data.csv"
        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip completely empty trailing lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 82
                self.assertEqual(
                    hive, "82",
                    f"Row {row_count}: Hive must be 82, got {hive}"
                )

                # 3. Direction must be East
                self.assertEqual(
                    direction, "East",
                    f"Row {row_count}: Direction must be East, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Total row count must match expected
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )

        print("[Test] Hive 82 CSV consistency passed.")


class TestHive83Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_83_data.csv

    Invariants enforced:

    1. Exactly 6770 non-empty data rows (excluding header).
    2. Each row has exactly 8 fields.
    3. Hive column is 83 in every row.
    4. Direction column is "West" in every row.
    5. Temperature field is non-empty in every row.
    6. Weight field may be empty or numeric.

    Fail-fast on first violation.
    """

    def test_hive_83_csv_structure(self):
        print("[Test] Hive 83 CSV consistency check...")

        path = "csv/hive_83_data.csv"
        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip trailing empty lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 83
                self.assertEqual(
                    hive, "83",
                    f"Row {row_count}: Hive must be 83, got {hive}"
                )

                # 3. Direction must be West
                self.assertEqual(
                    direction, "West",
                    f"Row {row_count}: Direction must be West, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Row count check
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )

        print("[Test] Hive 83 CSV consistency passed.")

class TestHive84Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_84_data.csv

    Invariants enforced:

    1. Exactly 6770 non-empty data rows (excluding header).
    2. Each row has exactly 8 fields.
    3. Hive column is 84 in every row.
    4. Direction column is "West" in every row.
    5. Temperature field is non-empty in every row.
    6. Weight field may be empty or numeric.

    Fail-fast on first violation.
    """

    def test_hive_84_csv_structure(self):
        print("[Test] Hive 84 CSV consistency check...")

        path = "csv/hive_84_data.csv"
        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip trailing empty lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 84
                self.assertEqual(
                    hive, "84",
                    f"Row {row_count}: Hive must be 84, got {hive}"
                )

                # 3. Direction must be West
                self.assertEqual(
                    direction, "West",
                    f"Row {row_count}: Direction must be West, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Row count check
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )

        print("[Test] Hive 84 CSV consistency passed.")        

class TestHive87Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_87_data.csv

    Invariants enforced:

    1. Exactly 6770 non-empty data rows (excluding header).
    2. Each row has exactly 8 fields.
    3. Hive column is 87 in every row.
    4. Direction column is "North" in every row.
    5. Temperature field is non-empty in every row.
    6. Weight field may be empty or numeric.

    Fail-fast on first violation.
    """

    def test_hive_87_csv_structure(self):
        print("[Test] Hive 87 CSV consistency check...")

        path = "csv/hive_87_data.csv"
        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip trailing empty lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 87
                self.assertEqual(
                    hive, "87",
                    f"Row {row_count}: Hive must be 87, got {hive}"
                )

                # 3. Direction must be North
                self.assertEqual(
                    direction, "North",
                    f"Row {row_count}: Direction must be North, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Row count check
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )

        print("[Test] Hive 87 CSV consistency passed.")

class TestHive90Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_90_data.csv

    Invariants enforced:

    1. Exactly 6770 non-empty data rows (excluding header).
    2. Each row has exactly 8 fields.
    3. Hive column is 90 in every row.
    4. Direction column is "South" in every row.
    5. Temperature field is non-empty in every row.
    6. Weight field may be empty or numeric.

    Fail-fast on first violation.
    """

    def test_hive_90_csv_structure(self):
        print("[Test] Hive 90 CSV consistency check...")

        path = "csv/hive_90_data.csv"
        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip trailing empty lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 90
                self.assertEqual(
                    hive, "90",
                    f"Row {row_count}: Hive must be 90, got {hive}"
                )

                # 3. Direction must be South
                self.assertEqual(
                    direction, "South",
                    f"Row {row_count}: Direction must be South, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Row count check
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )

        print("[Test] Hive 90 CSV consistency passed.")


class TestHive94Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_94_data.csv

    Invariants enforced:

    1. Exactly 6770 non-empty data rows (excluding header).
    2. Each row has exactly 8 fields.
    3. Hive column is 94 in every row.
    4. Direction column is "South" in every row.
    5. Temperature field is non-empty in every row.
    6. Weight field may be empty or numeric.

    Fail-fast on first violation.
    """

    def test_hive_94_csv_structure(self):
        print("[Test] Hive 94 CSV consistency check...")

        path = "csv/hive_94_data.csv"
        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip trailing empty lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 94
                self.assertEqual(
                    hive, "94",
                    f"Row {row_count}: Hive must be 94, got {hive}"
                )

                # 3. Direction must be South
                self.assertEqual(
                    direction, "South",
                    f"Row {row_count}: Direction must be South, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Row count check
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )

        print("[Test] Hive 94 CSV consistency passed.")


class TestHive94Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_94_data.csv

    Invariants enforced:

    1. Exactly 6770 non-empty data rows (excluding header).
    2. Each row has exactly 8 fields.
    3. Hive column is 94 in every row.
    4. Direction column is "South" in every row.
    5. Temperature field is non-empty in every row.
    6. Weight field may be empty or numeric.

    Fail-fast on first violation.
    """

    def test_hive_94_csv_structure(self):
        print("[Test] Hive 94 CSV consistency check...")

        path = "csv/hive_94_data.csv"
        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip trailing empty lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 94
                self.assertEqual(
                    hive, "94",
                    f"Row {row_count}: Hive must be 94, got {hive}"
                )

                # 3. Direction must be South
                self.assertEqual(
                    direction, "South",
                    f"Row {row_count}: Direction must be South, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Row count check
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )

        print("[Test] Hive 94 CSV consistency passed.")


class TestHive97Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_97_data.csv

    Invariants enforced:

    1. Exactly 6770 non-empty data rows (excluding header).
    2. Each row has exactly 8 fields.
    3. Hive column is 97 in every row.
    4. Direction column is "South" in every row.
    5. Temperature field is non-empty in every row.
    6. Weight field may be empty or numeric.

    Fail-fast on first violation.
    """

    def test_hive_97_csv_structure(self):
        print("[Test] Hive 97 CSV consistency check...")

        path = "csv/hive_97_data.csv"
        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip trailing empty lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 97
                self.assertEqual(
                    hive, "97",
                    f"Row {row_count}: Hive must be 97, got {hive}"
                )

                # 3. Direction must be South
                self.assertEqual(
                    direction, "South",
                    f"Row {row_count}: Direction must be South, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Row count check
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )

        print("[Test] Hive 97 CSV consistency passed.")

class TestHive99Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_99_data.csv

    Invariants enforced:

    1. Exactly 6770 non-empty data rows (excluding header).
    2. Each row has exactly 8 fields.
    3. Hive column is 99 in every row.
    4. Direction column is "West" in every row.
    5. Temperature field is non-empty in every row.
    6. Weight field may be empty or numeric.

    Fail-fast on first violation.
    """

    def test_hive_99_csv_structure(self):
        print("[Test] Hive 99 CSV consistency check...")

        path = "csv/hive_99_data.csv"
        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip trailing empty lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 99
                self.assertEqual(
                    hive, "99",
                    f"Row {row_count}: Hive must be 99, got {hive}"
                )

                # 3. Direction must be West
                self.assertEqual(
                    direction, "West",
                    f"Row {row_count}: Direction must be West, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Row count check
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )

        print("[Test] Hive 99 CSV consistency passed.")        

class TestHive103Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_103_data.csv

    This test enforces the following invariants:

    1. The file must contain exactly 6770 non-empty data rows
       (excluding the header line).
    2. Every data row must contain exactly 8 comma-separated fields.
    3. The hive column must be 103 in every row.
    4. The direction column must be "East" in every row.
    5. The temperature field must be non-empty in every row.
    6. The weight field may be empty or numeric (no constraint on count).

    The test fails immediately on the first violation.
    """

    def test_hive_103_csv_structure(self):
        print("[Test] Hive 103 CSV consistency check...")
        path = "csv/hive_103_data.csv"

        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip completely empty trailing lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 103
                self.assertEqual(
                    hive, "103",
                    f"Row {row_count}: Hive must be 103, got {hive}"
                )

                # 3. Direction must be East
                self.assertEqual(
                    direction, "East",
                    f"Row {row_count}: Direction must be East, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Total row count must match expected
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )
        print("[Test] Hive 103 CSV consistency passed.")


class TestHive104Consistency(unittest.TestCase):
    """
    Structural consistency test for the real dataset:
    csv/hive_104_data.csv

    This test enforces the following invariants:

    1. The file must contain exactly 6770 non-empty data rows
       (excluding the header line).
    2. Every data row must contain exactly 8 comma-separated fields.
    3. The hive column must be 104 in every row.
    4. The direction column must be "North" in every row.
    5. The temperature field must be non-empty in every row.
    6. The weight field may be empty or numeric (no constraint on count).

    The test fails immediately on the first violation.
    """

    def test_hive_104_csv_structure(self):
        print("[Test] Hive 104 CSV consistency check...")
        path = "csv/hive_104_data.csv"

        expected_rows = 6770
        row_count = 0

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            # Skip header
            header = next(reader)

            for row in reader:

                # Skip completely empty trailing lines
                if not row or all(field.strip() == "" for field in row):
                    continue

                row_count += 1

                # 1. Exactly 8 fields
                self.assertEqual(
                    len(row), 8,
                    f"Row {row_count}: Expected 8 fields, got {len(row)}"
                )

                hive = row[0].strip()
                direction = row[1].strip()
                temp = row[6].strip()

                # 2. Hive must be 104
                self.assertEqual(
                    hive, "104",
                    f"Row {row_count}: Hive must be 104, got {hive}"
                )

                # 3. Direction must be North
                self.assertEqual(
                    direction, "North",
                    f"Row {row_count}: Direction must be North, got {direction}"
                )

                # 4. Temperature must be present
                self.assertNotEqual(
                    temp, "",
                    f"Row {row_count}: Temperature field is empty"
                )

        # 5. Total row count must match expected
        self.assertEqual(
            row_count, expected_rows,
            f"Expected {expected_rows} rows, found {row_count}"
        )
        print("[Test] Hive 104 CSV consistency passed.")

if __name__ == "__main__":
    unittest.main()

