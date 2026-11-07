from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    window,
    count,
    sum as spark_sum,
    to_timestamp,
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
)

spark = (
    SparkSession.builder
    .appName("WindowedStreamingAggregation")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("event_time", StringType(), True),
])

print("=" * 70)
print("WINDOWED STREAMING AGGREGATIONS")
print("=" * 70)

kafka_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka-local:29092")
    .option("subscribe", "orders")
    .option("startingOffsets", "latest")
    .load()
)

parsed_stream = (
    kafka_stream
    .select(
        from_json(col("value").cast("string"), schema).alias("order")
    )
    .select("order.*")
    .withColumn(
        "event_timestamp",
        to_timestamp(col("event_time"))
    )
)

windowed_stream = (
    parsed_stream
    .groupBy(
        window(
            col("event_timestamp"),
            "10 seconds"
        )
    )
    .agg(
        count("*").alias("order_count"),
        spark_sum("amount").alias("total_amount")
    )
)

result = windowed_stream.select(
    col("window.start").alias("window_start"),
    col("window.end").alias("window_end"),
    col("order_count"),
    col("total_amount")
)

print("Connected to Kafka topic: orders")
print("Applying 10-second event-time windows")
print("Calculating order count and total amount")
print("Waiting for streaming events...")
print("Press Ctrl+C to stop.")
print("=" * 70)

query = (
    result.writeStream
    .format("console")
    .outputMode("update")
    .option("truncate", "false")
    .start()
)

query.awaitTermination()