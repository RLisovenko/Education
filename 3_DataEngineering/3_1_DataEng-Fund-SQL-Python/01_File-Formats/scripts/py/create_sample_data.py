"""
File: create_sample_data.py
Performed by: R. Lisovenko
Date: 07-10-2026

Description:
Creates sample sales data, converts the order_date column to datetime format,
and saves the dataset as a CSV file.
"""

import pandas as pd


# Constants
CSV_OUTPUT_FILE = "data/csv/sales_data.csv"
JSON_OUTPUT_FILE = "data/json/sales_data.json"
PARQUET_OUTPUT_FILE = "data/parquet/sales_data.parquet"

SALES_DATA = {
    "order_id": [1001, 1002, 1003, 1004, 1005],
    "customer_name": [
        "Alice Johnson",
        "Rahul Sharma",
        "Priya Nair",
        "John Thomas",
        "Sneha Patel"
    ],
    "product": [
        "Laptop",
        "Mouse",
        "Keyboard",
        "Monitor",
        "Webcam"
    ],
    "category": [
        "Electronics",
        "Accessories",
        "Accessories",
        "Electronics",
        "Accessories"
    ],
    "quantity": [1, 2, 1, 2, 3],
    "unit_price": [75000, 800, 1500, 18000, 2500],
    "city": [
        "Bengaluru",
        "Mumbai",
        "Chennai",
        "Hyderabad",
        "Pune"
    ],
    "order_date": [
        "2026-08-01",
        "2026-08-02",
        "2026-08-02",
        "2026-08-03",
        "2026-08-04"
    ]
}

# Create DataFrame
sales_data = pd.DataFrame(SALES_DATA)

# Convert date column
sales_data["order_date"] = pd.to_datetime(sales_data["order_date"])

# Save CSV
sales_data.to_csv(CSV_OUTPUT_FILE,index=False)
# Save JSON
sales_data.to_json(JSON_OUTPUT_FILE,orient="records", indent=2, date_format="iso")
# Save PARQUET
df =sales_data.to_parquet(PARQUET_OUTPUT_FILE,index=False)
print(df)
df = pd.read_parquet(PARQUET_OUTPUT_FILE)
print(df)