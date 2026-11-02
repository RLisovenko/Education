"""Optional snapshot/update/schema evolution exercise. Modifies a separate demo table only."""
from common import spark_session

spark=spark_session("NovaForge_Iceberg_History_Demo")
SOURCE="demo.manufacturing.manufacturing_production_metrics"
DEMO="demo.manufacturing.production_quality_events_demo"
try:
    source=spark.table(SOURCE).limit(4)
    source.writeTo(DEMO).using("iceberg").createOrReplace()
    print("Created isolated demo table")
    first=spark.table(DEMO).select("order_id").first().order_id
    spark.sql(f"UPDATE {DEMO} SET rejected_units = rejected_units + 1 WHERE order_id = '{first}'")
    spark.sql(f"ALTER TABLE {DEMO} ADD COLUMNS (machine_temperature_avg DOUBLE)")
    spark.sql(f"UPDATE {DEMO} SET machine_temperature_avg = 64.5 WHERE order_id = '{first}'")
    print("ICEBERG SNAPSHOTS")
    spark.sql(f"SELECT snapshot_id, operation, committed_at FROM {DEMO}.snapshots").show(truncate=False)
    print("SCHEMA EVOLUTION: machine_temperature_avg added")
    spark.table(DEMO).show(truncate=False)
finally:
    spark.stop()
