"""Read CSV/JSON/Parquet, apply validation and standardization, write PostgreSQL raw tables."""
import argparse
from pyspark.sql.functions import (
    col, trim, upper, regexp_replace, to_date, to_timestamp, lit
)
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType
)
from common import spark_session, write_jdbc

PATH = "/opt/project/data/raw"
parser = argparse.ArgumentParser()
parser.add_argument("--batch-date", default=None,
                    help="Optional YYYY-MM-DD; replaces raw fact sources with that day's records")
args = parser.parse_args()
spark = spark_session("NovaForge_Manufacturing_Staging")

def csv_source(file, names):
    schema = StructType([StructField(name, StringType(), True) for name in names])
    return (spark.read.option("header", True)
            .schema(schema)
            .csv(f"{PATH}/{file}"))

def clean_id(name):
    return upper(trim(col(name)))

def stage(name, frame):
    n = frame.count()
    if n == 0:
        raise RuntimeError(f"No rows available for raw.{name}")
    print(f"Writing raw.{name}: {n} records")
    # TRUNCATE preserves existing PostgreSQL table identities and dbt view dependencies.
    write_jdbc(frame, f"raw.{name}")

try:
    orders = csv_source("production_orders.csv", [
        "order_id","facility_id","line_id","product_id",
        "production_date","production_status","planned_units"])
    orders = (orders
        .withColumn("order_id", clean_id("order_id"))
        .withColumn("facility_id", clean_id("facility_id"))
        .withColumn("line_id", clean_id("line_id"))
        .withColumn("product_id", clean_id("product_id"))
        .withColumn("production_date", to_date("production_date"))
        .withColumn("planned_units", col("planned_units").cast("int"))
        .withColumn("production_status", regexp_replace(upper(trim(col("production_status"))), r"[ -]+", "_"))
        .filter(col("order_id").isNotNull() & (col("order_id") != ""))
        .filter(col("production_date").isNotNull())
        .filter(col("planned_units") > 0)
        .dropDuplicates(["order_id"]))
    if args.batch_date:
        import datetime
        datetime.date.fromisoformat(args.batch_date)
        orders = orders.filter(col("production_date") == lit(args.batch_date).cast("date"))
    if orders.count() == 0:
        raise RuntimeError("No orders found for selected batch date")

    ids = orders.select("order_id")
    operations_schema = StructType([
        StructField("operation_id", StringType()),StructField("order_id", StringType()),
        StructField("machine_id", StringType()),StructField("operation_at", StringType()),
        StructField("run_minutes", IntegerType()),StructField("downtime_minutes", IntegerType()),
        StructField("energy_consumption_kwh", DoubleType()),
    ])
    ops = (spark.read.schema(operations_schema).json(f"{PATH}/machine_operations.jsonl")
        .withColumn("operation_id", clean_id("operation_id"))
        .withColumn("order_id", clean_id("order_id"))
        .withColumn("machine_id", clean_id("machine_id"))
        .withColumn("operation_at", to_timestamp("operation_at"))
        .filter(col("operation_id").isNotNull())
        .filter(col("run_minutes") >= 0)
        .dropDuplicates(["operation_id"])
        .join(ids, "order_id", "inner"))

    quality = (spark.read.parquet(f"{PATH}/quality_inspections.parquet")
        .withColumn("inspection_id", clean_id("inspection_id"))
        .withColumn("order_id", clean_id("order_id"))
        .withColumn("inspection_at", to_timestamp("inspection_at"))
        .filter(col("inspection_id").isNotNull())
        .filter(col("inspected_units") > 0)
        .filter((col("rejected_units") >= 0) & (col("rejected_units") <= col("inspected_units")))
        .dropDuplicates(["inspection_id"])
        .join(ids, "order_id", "inner"))

    def ref(file, fields, casts=None):
        frame = csv_source(file, fields)
        for field in fields:
            if field.endswith("_id"):
                frame=frame.withColumn(field, clean_id(field))
        for field, dtype in (casts or {}).items():
            if dtype == "date":
                frame=frame.withColumn(field, to_date(col(field)))
            else:
                frame=frame.withColumn(field, col(field).cast(dtype))
        return frame.dropDuplicates([fields[0]])

    stage("facilities", ref("facilities.csv",["facility_id","facility_name","region"]))
    stage("production_lines", ref("production_lines.csv",["line_id","facility_id","line_name"]))
    stage("machines", ref("machines.csv",["machine_id","line_id","machine_type"]))
    stage("products", ref("products.csv",["product_id","product_name","product_family"]))
    stage("maintenance_records", ref("maintenance_records.csv",[
        "maintenance_id","machine_id","maintenance_date","downtime_minutes","maintenance_type"],
        {"maintenance_date":"date","downtime_minutes":"int"}))
    stage("production_orders", orders)
    stage("machine_operations", ops)
    stage("quality_inspections", quality)
    print("PYSPARK SOURCE PROCESSING COMPLETED SUCCESSFULLY")
finally:
    spark.stop()
