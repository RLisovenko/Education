import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

orders = [
    {"order_id": "ORD201", "customer": "Asha", "amount": 450.00, "status": "CREATED"},
    {"order_id": "ORD202", "customer": "Rahul", "amount": 1450.50, "status": "CREATED"},
    {"order_id": "ORD203", "customer": "Meera", "amount": 799.00, "status": "CREATED"},
    {"order_id": "ORD204", "customer": "Vikram", "amount": 2250.75, "status": "CREATED"},
    {"order_id": "ORD205", "customer": "Neha", "amount": 1100.00, "status": "CREATED"},
]

print("=" * 65)
print("STREAMING FILTER AND ENRICHMENT PRODUCER")
print("=" * 65)

for order in orders:
    metadata = producer.send("orders", value=order).get(timeout=10)

    print(
        f"Published {order['order_id']} | "
        f"Amount: {order['amount']} | "
        f"Partition: {metadata.partition} | "
        f"Offset: {metadata.offset}"
    )

    time.sleep(2)

producer.flush()
producer.close()

print("=" * 65)
print("All streaming order events published successfully.")
print("=" * 65)