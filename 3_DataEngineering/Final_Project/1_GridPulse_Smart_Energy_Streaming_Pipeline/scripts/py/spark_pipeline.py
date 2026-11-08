"""Kafka -> Spark Structured Streaming -> validation/quarantine + windows.

Run ONLY inside the Spark Docker image using the matching Kafka connector package.
"""
import argparse
from functools import partial

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg, col, concat_ws, count, from_json, length, lit, lower, round as spark_round,
    sum as spark_sum, to_timestamp, trim, upper, when, window,
)
from pyspark.sql.types import (
    DoubleType, StringType, StructField, StructType,
)

from sink import initialize_database, write_events_batch, write_windows_batch

TOPIC = "gridpulse-smart-meter-events"

EVENT_SCHEMA = StructType([
    StructField("event_id", StringType(), True),
    StructField("meter_id", StringType(), True),
    StructField("region", StringType(), True),
    StructField("energy_usage_kwh", DoubleType(), True),
    StructField("voltage", DoubleType(), True),
    StructField("device_status", StringType(), True),
    StructField("event_timestamp", StringType(), True),
])


def build_events(spark):
    source = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka-local:29092")
        .option("subscribe", TOPIC)
        .option("startingOffsets", "earliest")
        .option("failOnDataLoss", "true")
        .load()
    )
    typed = (
        source.select(
            col("key").cast("string").alias("kafka_key"),
            col("value").cast("string").alias("raw_json"),
            "topic", "partition", "offset",
        )
        .withColumn("payload", from_json(col("raw_json"), EVENT_SCHEMA))
        .withColumn("event_id", col("payload.event_id"))
        .withColumn("meter_id", col("payload.meter_id"))
        .withColumn("region", upper(trim(col("payload.region"))))
        .withColumn("energy_usage_kwh", col("payload.energy_usage_kwh"))
        .withColumn("voltage", col("payload.voltage"))
        .withColumn("device_status", upper(trim(col("payload.device_status"))))
        .withColumn("event_timestamp", to_timestamp(col("payload.event_timestamp")))
    )

    error_conditions = [
        when(col("payload").isNull(), lit("malformed_json")),
        when(col("event_id").isNull() | (length(trim(col("event_id"))) == 0),
             lit("missing_event_id")),
        when(col("meter_id").isNull() | (length(trim(col("meter_id"))) == 0),
             lit("missing_meter_id")),
        when(col("region").isNull() | (length(col("region")) == 0),
             lit("missing_region")),
        when(col("kafka_key").isNull() | (col("kafka_key") != col("meter_id")),
             lit("kafka_key_meter_mismatch")),
        when(col("energy_usage_kwh").isNull() |
             (col("energy_usage_kwh") < 0) | (col("energy_usage_kwh") > 100),
             lit("invalid_energy_usage_kwh")),
        when(col("voltage").isNull() | (col("voltage") < 190) |
             (col("voltage") > 250), lit("invalid_voltage")),
        when(col("device_status").isNull() |
             (~col("device_status").isin("ONLINE", "OFFLINE", "MAINTENANCE")),
             lit("unsupported_device_status")),
        when(col("event_timestamp").isNull(), lit("invalid_event_timestamp")),
    ]
    return (
        typed.withColumn("validation_error", concat_ws("; ", *error_conditions))
        .withColumn("is_valid", length(col("validation_error")) == 0)
        .withColumn("usage_category", when(col("energy_usage_kwh") >= 10,
                                           lit("HIGH")).otherwise(lit("NORMAL")))
        .withColumn("voltage_status", when(col("voltage").between(210, 240),
                                         lit("NORMAL")).otherwise(lit("CHECK")))
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fail-on-offset", type=int, default=-1,
                        help="Controlled one-time failure: rerun without this option")
    args = parser.parse_args()

    spark = (
        SparkSession.builder.appName("GridPulseReliableSmartEnergy")
        .master("local[2]")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    initialize_database()
    stream = build_events(spark)

    # Separate, persistent checkpoints for the independent queries.
    event_query = (
        stream.select(
            "event_id", "meter_id", "region", "energy_usage_kwh", "voltage",
            "device_status", "event_timestamp", "usage_category", "voltage_status",
            "validation_error", "is_valid", "topic", "partition", "offset", "raw_json",
        ).writeStream
        .foreachBatch(partial(write_events_batch, fail_on_offset=args.fail_on_offset))
        .option("checkpointLocation", "/opt/project/checkpoints/events")
        .outputMode("append")
        .trigger(processingTime="5 seconds")
        .start()
    )

    # A watermark bounds late-event state. Deduplication by business event_id
    # prevents repeated Kafka deliveries from inflating finalized aggregates.
    deduplicated = (
        stream.filter(col("is_valid"))
        .withWatermark("event_timestamp", "2 minutes")
        .dropDuplicatesWithinWatermark(["event_id"])
    )
    aggregates = (
        deduplicated.groupBy(window(col("event_timestamp"), "5 minutes"), col("region"))
        .agg(
            count(lit(1)).alias("reading_count"),
            spark_round(spark_sum("energy_usage_kwh"), 3).alias("total_kwh"),
            spark_round(avg("voltage"), 2).alias("avg_voltage"),
            spark_sum(when(col("energy_usage_kwh") >= 10, lit(1)).otherwise(lit(0)))
            .alias("high_usage_count"),
        )
        .select(
            "region", col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            "reading_count", "total_kwh", "avg_voltage", "high_usage_count",
        )
    )
    window_query = (
        aggregates.writeStream.foreachBatch(write_windows_batch)
        .outputMode("append")
        .option("checkpointLocation", "/opt/project/checkpoints/windows")
        .trigger(processingTime="5 seconds")
        .start()
    )
    print("GridPulse queries started: events + 5-minute regional windows", flush=True)
    print("Watermark: 2 minutes | Kafka topic:", TOPIC, flush=True)
    print("Check results with: py .\\inspect_results.py", flush=True)
    print("Press Ctrl+C to stop; preserve checkpoints/ for restart.", flush=True)
    try:
        spark.streams.awaitAnyTermination()
    finally:
        for query in (event_query, window_query):
            if query.isActive:
                query.stop()
        spark.stop()


if __name__ == "__main__":
    main()
