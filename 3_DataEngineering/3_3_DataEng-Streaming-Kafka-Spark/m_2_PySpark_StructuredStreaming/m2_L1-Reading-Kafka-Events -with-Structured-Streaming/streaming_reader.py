from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = (
    SparkSession.builder
    .appName("KafkaStructuredStreamingReader")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("=" * 70)
print("SPARK STRUCTURED STREAMING - KAFKA READER")
print("=" * 70)

kafka_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka-local:29092")
    .option("subscribe", "orders")
    .option("startingOffsets", "latest")
    .load()
)

events = kafka_stream.select(
    col("key").cast("string").alias("key"),
    col("value").cast("string").alias("value"),
    col("topic"),
    col("partition"),
    col("offset"),
    col("timestamp"),
)

print("Connected to Kafka topic: orders")
print("Waiting for streaming events...")
print("Press Ctrl+C to stop.")
print("=" * 70)

query = (
    events.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", "false")
    .start()
)

query.awaitTermination()