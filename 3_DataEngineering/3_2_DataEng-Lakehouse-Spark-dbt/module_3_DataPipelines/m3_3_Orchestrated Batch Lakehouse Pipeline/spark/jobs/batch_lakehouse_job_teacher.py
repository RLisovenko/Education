from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    upper,
    initcap,
    coalesce,
    lit,
    current_timestamp,
    round as spark_round,
    when,
)


INPUT_PATH = "/opt/project/data/raw/daily_shipments.csv"
TABLE_NAME = "local.logistics.shipment_analytics"


spark = (
    SparkSession.builder
    .appName("LogisticsShipmentLakehousePipeline")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


print("=" * 72)
print("ORCHESTRATED LOGISTICS BATCH LAKEHOUSE PIPELINE")
print("=" * 72)


print("\nREADING DAILY SHIPMENT BATCH")
print("-" * 72)

raw_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(INPUT_PATH)
)

raw_df.show(truncate=False)


print("\nVALIDATING SHIPMENT DATA")
print("-" * 72)

required_columns = {
    "shipment_id",
    "distribution_center",
    "destination",
    "package_count",
    "shipping_cost",
    "shipment_status",
    "shipment_date",
}

missing_columns = required_columns - set(raw_df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {sorted(missing_columns)}"
    )

record_count = raw_df.count()

if record_count == 0:
    raise ValueError("Shipment batch contains no records")

print(f"Source validation passed for {record_count} shipment records")


print("\nTRANSFORMING SHIPMENT DATA")
print("-" * 72)

curated_df = (
    raw_df
    .withColumn(
        "distribution_center",
        initcap(trim(col("distribution_center")))
    )
    .withColumn(
        "destination",
        initcap(trim(col("destination")))
    )
    .withColumn(
        "shipment_status",
        upper(trim(col("shipment_status")))
    )
    .withColumn(
        "package_count",
        col("package_count").cast("int")
    )
    .withColumn(
        "shipping_cost",
        coalesce(
            col("shipping_cost").cast("double"),
            lit(0.0)
        )
    )
    .withColumn(
        "cost_per_package",
        when(
            col("package_count") > 0,
            spark_round(
                col("shipping_cost") / col("package_count"),
                2
            )
        ).otherwise(lit(0.0))
    )
    .withColumn(
        "processed_at",
        current_timestamp()
    )
)

curated_df.show(truncate=False)


print("\nCREATING ICEBERG NAMESPACE")
print("-" * 72)

spark.sql(
    "CREATE NAMESPACE IF NOT EXISTS local.logistics"
)


print("\nWRITING SHIPMENT DATA TO ICEBERG")
print("-" * 72)

(
    curated_df.writeTo(TABLE_NAME)
    .using("iceberg")
    .createOrReplace()
)

print(f"Iceberg table created: {TABLE_NAME}")


print("\nVALIDATING LAKEHOUSE TABLE")
print("-" * 72)

result_df = spark.sql(
    f"""
    SELECT
        shipment_id,
        distribution_center,
        destination,
        package_count,
        shipping_cost,
        cost_per_package,
        shipment_status,
        shipment_date
    FROM {TABLE_NAME}
    ORDER BY shipment_id
    """
)

result_df.show(truncate=False)


final_count = result_df.count()

if final_count != 8:
    raise ValueError(
        f"Expected 8 shipment records but found {final_count}"
    )

print(f"Validated {final_count} curated shipment records")


print("\nSHIPMENT STATUS SUMMARY")
print("-" * 72)

spark.sql(
    f"""
    SELECT
        shipment_status,
        COUNT(*) AS shipment_count,
        ROUND(SUM(shipping_cost), 2) AS total_shipping_cost
    FROM {TABLE_NAME}
    GROUP BY shipment_status
    ORDER BY shipment_status
    """
).show(truncate=False)


print("\nICEBERG SNAPSHOT VALIDATION")
print("-" * 72)

spark.sql(
    f"""
    SELECT
        snapshot_id,
        operation
    FROM {TABLE_NAME}.snapshots
    """
).show(truncate=False)


print("=" * 72)
print("LOGISTICS BATCH LAKEHOUSE PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 72)


spark.stop()
