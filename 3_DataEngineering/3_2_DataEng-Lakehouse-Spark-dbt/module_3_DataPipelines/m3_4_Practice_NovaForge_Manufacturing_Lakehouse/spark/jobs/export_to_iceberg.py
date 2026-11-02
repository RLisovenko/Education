"""Publish the dbt manufacturing fact model to Iceberg in MinIO, idempotently by order_id."""
from pyspark.sql.functions import col, current_timestamp
from common import spark_session, load_jdbc

TABLE = "demo.manufacturing.manufacturing_production_metrics"
spark = spark_session("NovaForge_Publish_Iceberg")
try:
    df = load_jdbc(spark, "marts.fact_production")
    df = (df.select(
        col("order_id").cast("string"),
        col("facility_id").cast("string"),
        col("line_id").cast("string"),
        col("product_id").cast("string"),
        col("production_date").cast("date"),
        col("production_status").cast("string"),
        col("planned_units").cast("int"),
        col("actual_units").cast("int"),
        col("rejected_units").cast("int"),
        col("defect_rate").cast("double"),
        col("runtime_minutes").cast("int"),
        col("downtime_minutes").cast("int"),
        col("production_duration_minutes").cast("int"),
        col("operation_count").cast("int"),
    ).withColumn("processed_at", current_timestamp()))
    count=df.count()
    if not count:
        raise ValueError("dbt mart fact_production is empty")
    spark.sql("CREATE NAMESPACE IF NOT EXISTS demo.manufacturing")
    exists=spark.catalog.tableExists(TABLE)
    if not exists:
        df.writeTo(TABLE).using("iceberg").create()
        print(f"CREATED ICEBERG TABLE: {TABLE}")
    else:
        df.createOrReplaceTempView("incoming_manufacturing")
        spark.sql(f"""
            MERGE INTO {TABLE} AS t
            USING incoming_manufacturing AS s
            ON t.order_id = s.order_id
            WHEN MATCHED THEN UPDATE SET *
            WHEN NOT MATCHED THEN INSERT *
        """)
        print(f"MERGED INTO ICEBERG TABLE: {TABLE}")
    print(f"ICEBERG PUBLISH SUCCESS: {count} source records")
    spark.sql(f"SELECT COUNT(*) AS total_records FROM {TABLE}").show()
finally:
    spark.stop()
