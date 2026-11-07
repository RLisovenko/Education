from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

spark = (
    SparkSession.builder
    .appName("FilteringAndEnrichingStreamingData")
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
print("FILTERING AND ENRICHING STREAMING DATA")
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
        from_json(col("value").cast("string"), schema).alias("order"),
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

filtered_stream = parsed_stream.filter(
    col("amount") >= 1000
)

enriched_stream = (
    filtered_stream
    .withColumn(
        "priority",
        when(col("amount") >= 2000, "CRITICAL")    
        .otherwise("HIGH")
    )
    .withColumn(
        "amount_band",
        when(col("amount") >= 2000, "2000+")
        .otherwise("1000-1999")
    )
)

final_stream = enriched_stream.select(
    "order_id",
    "customer",
    "amount",
    "status",
    "priority",
    "amount_band",
    "partition",
    "offset",
    "timestamp"
)

print("Connected to Kafka topic: orders")
print("Filtering orders with amount >= 1000")
print("Enriching retained orders with priority and amount band")
print("Waiting for streaming events...")
print("Press Ctrl+C to stop.")
print("=" * 70)

query = (
    final_stream.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", "false")
    .start()
)

query.awaitTermination()