# ------------------------------------------------------------
# Course: Lakehouse Data Pipelines with Spark and dbt
# Script: create_parquet_data.py
# Performed by: R. Lisovenko
# Started: 27.10.2026
# Description: Convert source CSV data to Parquet format.
# ------------------------------------------------------------

from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType,
)

# Resolve paths relative to the project directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = PROJECT_ROOT / "data" / "csv" / "operations_data.csv"
PARQUET_PATH = PROJECT_ROOT / "data" / "parquet" / "operations_data.parquet"

# Define the source data schema.
schema = StructType([
    StructField("record_id", IntegerType(), False),
    StructField("source_system", StringType(), True),
    StructField("category", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("amount", DoubleType(), True),
    StructField("event_date", StringType(), True),
])

spark = (
    SparkSession.builder
    .appName("CreateParquetData")
    .master("local[1]")
    .config("spark.driver.memory", "1g")
    .config("spark.sql.shuffle.partitions", "1")
    .getOrCreate()
)

try:
    spark.sparkContext.setLogLevel("ERROR")

    # Read source CSV data.
    df = (
        spark.read
        .option("header", True)
        .schema(schema)
        .csv(str(CSV_PATH))
    )

    # Write data in Parquet format.
    df.coalesce(1).write.mode("overwrite").parquet(str(PARQUET_PATH))

    print("Parquet data created successfully.", flush=True)
    print(f"Output directory: {PARQUET_PATH}", flush=True)

finally:
    # Release Spark resources.
    spark.stop()
    print("SparkSession stopped.", flush=True)