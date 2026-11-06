import json

from kafka import KafkaConsumer


consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="order-processing-group",
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

print("=" * 60)
print("PYTHON KAFKA CONSUMER")
print("=" * 60)
print("Listening for order events...")
print("Press Ctrl+C to stop.")
print("=" * 60)

try:
    for message in consumer:
        order = message.value

        print(
            f"Received {order['order_id']} | "
            f"Customer: {order['customer']} | "
            f"Amount: {order['amount']} | "
            f"Status: {order['status']} | "
            f"Partition: {message.partition} | "
            f"Offset: {message.offset}"
        )

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()