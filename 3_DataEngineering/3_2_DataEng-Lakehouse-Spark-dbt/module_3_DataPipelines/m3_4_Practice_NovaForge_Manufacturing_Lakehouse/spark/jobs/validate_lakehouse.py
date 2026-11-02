"""Validate published Iceberg records against PostgreSQL/dbt and inspect snapshots."""
from common import spark_session, load_jdbc

TABLE = "demo.manufacturing.manufacturing_production_metrics"
spark=spark_session("NovaForge_Validate_Lakehouse")
try:
    expected=load_jdbc(spark, "marts.fact_production").count()
    actual=spark.sql(f"SELECT COUNT(*) AS n FROM {TABLE}").first().n
    if expected <= 0:
        raise RuntimeError("dbt fact_production is unexpectedly empty")
    if actual < expected:
        raise RuntimeError(f"Iceberg has {actual} rows, but current dbt mart has {expected}")
    duplicate_count=spark.sql(f"""
        SELECT COUNT(*) AS n FROM (
          SELECT order_id FROM {TABLE} GROUP BY order_id HAVING COUNT(*) > 1
        )
    """).first().n
    if duplicate_count:
        raise RuntimeError(f"Iceberg contains {duplicate_count} duplicated order identifiers")
    bad_values=spark.sql(f"""
       SELECT COUNT(*) AS n FROM {TABLE}
       WHERE rejected_units < 0 OR defect_rate < 0 OR defect_rate > 1
    """).first().n
    if bad_values:
        raise RuntimeError("Iceberg contains invalid manufacturing metrics")
    snapshots=spark.sql(f"SELECT snapshot_id, operation, committed_at FROM {TABLE}.snapshots")
    if not snapshots.take(1):
        raise RuntimeError("Iceberg table has no snapshots")
    print(f"VALIDATION SUCCESS: Iceberg {actual} rows, current mart {expected} rows")
    snapshots.show(truncate=False)
finally:
    spark.stop()
