# ------------------------------------------------------------
# Script: spark_shutdown_test.py
# Purpose: Diagnose Spark shutdown behavior on Windows.
# ------------------------------------------------------------

from pyspark.sql import SparkSession

print("Starting Spark...", flush=True)

spark = (
    SparkSession.builder
    .appName("SparkShutdownTest")
    .master("local[1]")
    .getOrCreate()
)

print("Spark started.", flush=True)

spark.stop()

print("Spark stopped.", flush=True)