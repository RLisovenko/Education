"""
File: inspect_formats.py
Performed by: R. Lisovenko
Date: 07-10-2026

Description:
Reads and inspects CSV, JSON, and Parquet files.
Displays dataset shape, column names, and data types.
"""

import pandas as pd
import folder_contents as fc


# Constants
CSV_FILE = "data/csv/sales_data.csv"
JSON_FILE = "data/json/sales_data.json"
PARQUET_FILE = "data/parquet/sales_data.parquet"


def inspect_data(data, format_name):
    print("\n" + "=" * 60)
    print(f"{format_name} FORMAT")
    print("=" * 60)

    print(f"Shape(rows, columns): {data.shape}")

    print("\nColumns:")
    print(data.columns.tolist())

    print("\nData Types:")
    print(data.dtypes)

if __name__ == "__main__":
    
    print("=" * 60)
    print("CSV, JSON, AND PARQUET FILE INSPECTION")
    print("=" * 60)

    # CSV
    csv_data = pd.read_csv(CSV_FILE)
    inspect_data(csv_data, "CSV")

    # JSON
    json_data = pd.read_json(JSON_FILE)
    inspect_data(json_data, "JSON")

    # Parquet
    parquet_data = pd.read_parquet(PARQUET_FILE)
    inspect_data(parquet_data, "PARQUET")
    print(parquet_data)

    fc.print_folder_contents("data")

    print("\n"+"=" * 60)
    print("FORMAT COMPARISION SUMMARY" )
    print("=" * 60)
