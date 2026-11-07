from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
)

spark = (
    SparkSession.builder
    .appName("CheckpointStreamRecovery")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("status", StringType(), True),
])

print("=" * 70)
print("STRUCTURED STREAMING CHECKPOINT RECOVERY")
print("=" * 70)

kafka_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka-local:29092")
    .option("subscribe", "checkpoint-orders")
    .option("startingOffsets", "earliest")
    .load()
)

parsed_stream = (
    kafka_stream
    .select(
        from_json(
            col("value").cast("string"),
            schema
        ).alias("order"),
        col("partition"),
        col("offset"),
        col("timestamp")
    )
    .select(
        "order.*",
        "partition",
        "offset",
        "timestamp"
    )
)

print("Connected to Kafka topic: checkpoint-orders")
print("Checkpoint directory: /opt/project/checkpoints")
print("Waiting for order events...")
print("Press Ctrl+C to simulate a stream interruption.")
print("=" * 70)

query = (
    parsed_stream.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", "false")
    .option(
        "checkpointLocation",
        "/opt/project/checkpoints"
    )
    .start()
)

query.awaitTermination()