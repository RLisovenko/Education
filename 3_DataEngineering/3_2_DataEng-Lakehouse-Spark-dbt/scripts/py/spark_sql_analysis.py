# Executor: R. Lisovenko
# Date: 28.10.2026

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SparkSQLAnalysis")
    .master("local[2]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("=" * 70)
print("ANALYSING DATA WITH SPARK SQL")
print("=" * 70)

operations_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/csv/operations.csv")
)

systems_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("data/csv/systems.csv")
)

print("\nOPERATIONS DATA")
print("-" * 70)
operations_df.show()

print("\nSYSTEMS DATA")
print("-" * 70)
systems_df.show()

# Create temporary SQL views from DataFrames for querying with Spark SQL / Создаём временные SQL-представления из DataFrame для выполнения запросов через Spark SQL

operations_df.createOrReplaceTempView("operations")
systems_df.createOrReplaceTempView("systems")

print("\nACTIVE RECORDS")
print("-" * 70)

active_df = spark.sql("""
    SELECT
        record_id,
        source_system,
        category,
        quantity,
        amount
    FROM operations
    WHERE status = 'ACTIVE'
    ORDER BY record_id
""")

active_df.show()

print("\nCATEGORY METRICS")
print("-" * 70)

category_metrics_df = spark.sql("""
    SELECT
        category,
        COUNT(*) AS record_count,
        SUM(quantity) AS total_quantity,
        SUM(quantity * amount) AS total_value
    FROM operations
    WHERE status = 'ACTIVE'
    GROUP BY category
    ORDER BY total_value DESC
""")

category_metrics_df.show()

print("\nSYSTEM OWNERSHIP JOIN")
print("-" * 70)

joined_df = spark.sql("""
    SELECT
        o.record_id,
        o.source_system,
        s.system_name,
        s.owner_team,
        o.category,
        o.quantity,
        o.amount,
        o.status
    FROM operations o
    INNER JOIN systems s
        ON o.source_system = s.source_system
    ORDER BY o.record_id
""")

joined_df.show(truncate=False)

print("\nSYSTEM-LEVEL METRICS")
print("-" * 70)

system_metrics_df = spark.sql("""
    SELECT
        s.system_name,
        s.owner_team,
        COUNT(*) AS record_count,
        SUM(o.quantity) AS total_quantity,
        ROUND(SUM(o.quantity * o.amount), 2) AS total_value
    FROM operations o
    INNER JOIN systems s
        ON o.source_system = s.source_system
    WHERE o.status = 'ACTIVE'
    GROUP BY
        s.system_name,
        s.owner_team
    ORDER BY total_value DESC
""")

system_metrics_df.show(truncate=False)

print("\nOVERALL METRICS")
print("-" * 70)

overall_metrics_df = spark.sql("""
    SELECT
        COUNT(*) AS total_records,
        SUM(quantity) AS total_quantity,
        ROUND(SUM(quantity * amount), 2) AS total_value,
        ROUND(AVG(amount), 2) AS average_amount
    FROM operations
    WHERE status = 'ACTIVE'
""")

overall_metrics_df.show()

print("=" * 70)
print("SPARK SQL ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

spark.stop()
