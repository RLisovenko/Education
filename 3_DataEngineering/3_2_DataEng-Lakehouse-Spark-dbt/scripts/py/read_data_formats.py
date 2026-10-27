# ------------------------------------------------------------
# Course: Lakehouse Data Pipelines with Spark and dbt
# Script: read_data_formats.py
# Performed by: R. Lisovenko
# Started: 27.10.2026
#
# Description:
# Read CSV, JSON, and Parquet files using an explicit schema.
# ------------------------------------------------------------

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType,
)

# Initialize a local SparkSession.
spark = (
    SparkSession.builder
    .appName("ReadDataFormats")
    .master("local[2]")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)

# Reduce unnecessary Spark log messages.
spark.sparkContext.setLogLevel("ERROR")

# Display the section header.
print("=" * 70)
print("READING CSV, JSON, AND PARQUET WITH PYSPARK")
print("=" * 70)

# Define an explicit schema for the source data.
schema = StructType([
    StructField("record_id", IntegerType(), False),
    StructField("source_system", StringType(), True),
    StructField("category", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("amount", DoubleType(), True),
    StructField("event_date", StringType(), True),
])

# ------------------------------------------------------------
# Read CSV data using an explicit schema.
# ------------------------------------------------------------

print("\nCSV FORMAT")
print("-" * 70)

csv_df = (
    spark.read
    .option("header", True)
    .schema(schema)
    .csv("data/csv/operations_data.csv")
)

# Display the CSV schema and records.
csv_df.printSchema()
csv_df.show()

# Count the number of CSV records.
print(f"CSV Row Count: {csv_df.count()}")


# ------------------------------------------------------------
# Read JSON data using the same explicit schema.
# ------------------------------------------------------------

print("\nJSON FORMAT")
print("-" * 70)

json_df = (
    spark.read
    .schema(schema)
    .json("data/json/operations_data.json")
)

# ------------------------------------------------------------
# Display JSON schema, records, and row count.
# ------------------------------------------------------------

json_df.printSchema()
json_df.show()
print(f"JSON Row Count: {json_df.count()}")


# ------------------------------------------------------------
# Read Parquet data.
# ------------------------------------------------------------

print("\nPARQUET FORMAT")
print("-" * 70)

parquet_df = spark.read.parquet(
    "data/parquet/operations_data.parquet"
)

# Display Parquet schema, records, and row count.
parquet_df.printSchema()
parquet_df.show()
print(f"Parquet Row Count: {parquet_df.count()}")


# ------------------------------------------------------------
# Compare CSV, JSON, and Parquet DataFrames.
# ------------------------------------------------------------

print("\nFORMAT COMPARISON")
print("-" * 70)

# Compare the number of columns.
print(f"CSV Columns     : {len(csv_df.columns)}")
print(f"JSON Columns    : {len(json_df.columns)}")
print(f"Parquet Columns : {len(parquet_df.columns)}")

# Compare the number of records.
print(f"CSV Rows        : {csv_df.count()}")
print(f"JSON Rows       : {json_df.count()}")
print(f"Parquet Rows    : {parquet_df.count()}")

# Display the completion message.
print("=" * 70)
print("ALL DATA FORMATS READ SUCCESSFULLY")
print("=" * 70)

# Stop the SparkSession and release resources.
spark.stop()