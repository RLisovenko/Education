# ------------------------------------------------------------
# Course: Lakehouse Data Pipelines with Spark and dbt
# Script: spark_setup_check.py
# Performed by: R. Lisovenko
# Started: 27.10.2026
# Description: Verify local PySpark environment and SparkSession.
# ------------------------------------------------------------
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("3_2_DataEng-Lakehouse-Spark-Setup")
    .master("local[1]") # all core use .master("local[*]")
    .config("spark.driver.memory", "1g")
    .config("spark.sql.shuffle.partitions", "1")
    .config("spark.default.parallelism", "1")
    .getOrCreate()
)

print("Spark version:", spark.version)
print("\nSOURCE DATAFRAME")

data = [(1, "Python"), (2, "PySpark"), (3, "Lakehouse")]

df = spark.createDataFrame(data, ["id", "technology"])
df.show()

#-------------------------
# Create a small distributed DataFrame.
data = [
    (1, "CSV", 120),
    (2, "JSON", 85),
    (3, "Parquet", 250),
    (4, "CSV", 175),
]

df = spark.createDataFrame(
    data,
    ["file_id", "format", "records"]
)

# Display the source DataFrame.
print("\nFILTERED DATAFRAME")
df.show()

# Stop the SparkSession and release Spark resources.
print("\nStopping Spark...", flush=True)

spark.stop()


# Confirm successful script completion.
print("\n" + 25 * "*")
print("SparkSession stopped successfully.", flush=True)
print(25 * "*")
# Diagnose whether Python exits after Spark shutdown.
import threading
print("Active threads:", threading.enumerate(), flush=True)