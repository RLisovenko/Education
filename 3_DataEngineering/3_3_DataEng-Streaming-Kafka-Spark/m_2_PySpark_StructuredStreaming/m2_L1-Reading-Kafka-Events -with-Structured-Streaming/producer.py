import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

events = [
    {
        "order_id": "STR001",
        "customer": "Asha",
        "amount": 1250.50,
        "status": "CREATED",
    },
    {
        "order_id": "STR002",
        "customer": "Rahul",
        "amount": 899.00,
        "status": "PAID",
    },
    {
        "order_id": "STR003",
        "customer": "Meera",
        "amount": 2100.75,
        "status": "SHIPPED",
    },
]

print("=" * 60)
print("STREAMING EVENT PRODUCER")
print("=" * 60)

for event in events:
    metadata = producer.send("orders", value=event).get(timeout=10)

    print(
        f"Published {event['order_id']} | "
        f"Partition: {metadata.partition} | "
        f"Offset: {metadata.offset}"
    )

    time.sleep(2)

producer.flush()
producer.close()

print("=" * 60)
print("Streaming events published successfully.")
print("=" * 60)