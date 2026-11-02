"""Convert the supplied JSON seed into a genuine Parquet source dataset."""
import os
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from common import spark_session

SEED = "/opt/project/data/seed/quality_inspections.jsonl"
TARGET = "/opt/project/data/raw/quality_inspections.parquet"
spark = spark_session("NovaForge_Bootstrap_Quality_Parquet")
try:
    schema = StructType([
        StructField("inspection_id", StringType()),
        StructField("order_id", StringType()),
        StructField("inspected_units", IntegerType()),
        StructField("rejected_units", IntegerType()),
        StructField("inspection_at", StringType()),
    ])
    source = spark.read.schema(schema).json(SEED)
    count = source.count()
    if count < 1:
        raise RuntimeError("Quality inspection seed is empty")
    source.coalesce(1).write.mode("overwrite").parquet(TARGET)
    print(f"PARQUET SOURCE READY: {TARGET} ({count} records)")
finally:
    spark.stop()
