import json
import os

from kafka import KafkaConsumer


consumer_name = os.getenv("CONSUMER_NAME", "consumer")

consumer = KafkaConsumer(
    "partitioned-orders",
    bootstrap_servers="localhost:9092",
    group_id="order-processing-group-demo",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    key_deserializer=lambda key: key.decode("utf-8") if key else None,
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

print("=" * 70)
print(f"KAFKA CONSUMER GROUP MEMBER: {consumer_name}")
print("=" * 70)
print("Waiting for partition assignments and order events...")
print("Press Ctrl+C to stop.")
print("=" * 70)

try:
    for message in consumer:
        order = message.value

        print(
            f"{consumer_name} received {order['order_id']} | "
            f"Key: {message.key} | "
            f"Partition: {message.partition} | "
            f"Offset: {message.offset}"
        )

except KeyboardInterrupt:
    print(f"\n{consumer_name} stopped.")

finally:
    consumer.close()