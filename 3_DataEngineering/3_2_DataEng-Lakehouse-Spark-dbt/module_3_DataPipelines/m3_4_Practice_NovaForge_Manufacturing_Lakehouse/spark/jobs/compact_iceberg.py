"""Optional Iceberg data-file compaction example for the isolated demo table."""
from common import spark_session
spark=spark_session("NovaForge_Iceberg_Compaction")
try:
    result=spark.sql("""
       CALL demo.system.rewrite_data_files(
         table => 'manufacturing.production_quality_events_demo',
         options => map('min-input-files','2')
       )
    """)
    result.show(truncate=False)
finally:
    spark.stop()
