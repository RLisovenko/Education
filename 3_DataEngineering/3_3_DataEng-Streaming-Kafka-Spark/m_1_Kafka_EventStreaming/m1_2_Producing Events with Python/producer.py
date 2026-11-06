import json
import time

from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

orders = [
    {
        "order_id": "ORD101",
        "customer": "Ananya",
        "amount": 1450.50,
        "status": "CREATED",
    },
    {
        "order_id": "ORD102",
        "customer": "Vikram",
        "amount": 799.00,
        "status": "CREATED",
    },
    {
        "order_id": "ORD103",
        "customer": "Neha",
        "amount": 2250.75,
        "status": "CREATED",
    },
]

print("=" * 60)
print("PYTHON KAFKA PRODUCER")
print("=" * 60)

for order in orders:
    future = producer.send("orders", value=order)
    metadata = future.get(timeout=10)

    print(
        f"Sent {order['order_id']} "
        f"to topic={metadata.topic}, "
        f"partition={metadata.partition}, "
        f"offset={metadata.offset}"
    )

    time.sleep(1)

producer.flush()
producer.close()

print("=" * 60)
print("All order events published successfully.")
print("=" * 60)