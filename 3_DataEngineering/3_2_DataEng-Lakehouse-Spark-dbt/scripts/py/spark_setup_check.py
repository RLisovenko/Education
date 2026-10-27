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
    .master("local[2]") # all core use .master("local[*]")
    .config("spark.driver.memory", "1g")       # Limit driver JVM heap to 1 GB.
    .config("spark.sql.shuffle.partitions", "2")  # Reduce shuffle partitions.
    .getOrCreate()
)

print("Spark version:", spark.version)

data = [(1, "Python"), (2, "PySpark"), (3, "Lakehouse")]

df = spark.createDataFrame(data, ["id", "technology"])

df.show()

# Stop the SparkSession and release Spark resources.
spark.stop()

# Confirm successful script completion.
print("PySpark environment check completed successfully.")