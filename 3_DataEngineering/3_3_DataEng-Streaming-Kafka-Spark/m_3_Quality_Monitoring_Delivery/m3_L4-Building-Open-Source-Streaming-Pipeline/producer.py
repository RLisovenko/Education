import json
import time
from kafka import KafkaProducer

TOPIC = "capstone-orders"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

events = [
    {
        "order_id": "CAP001",
        "customer": "Asha",
        "amount": 1250.50,
        "status": "CREATED",
    },
    {
        "order_id": "CAP002",
        "customer": "Rahul",
        "amount": 899.00,
        "status": "PAID",
    },
    {
        "order_id": "CAP003",
        "customer": "",
        "amount": 650.00,
        "status": "CREATED",
    },
    {
        "order_id": "CAP004",
        "customer": "Vikram",
        "amount": 1750.00,
        "status": "PAID",
    },
    {
        "order_id": "CAP005",
        "customer": "Meera",
        "amount": 2200.00,
        "status": "CREATED",
        "simulate_failure": True,
    },
    {
        "order_id": "CAP006",
        "customer": "Neha",
        "amount": 2450.25,
        "status": "SHIPPED",
    },
    {
        "order_id": "CAP007",
        "customer": "Arjun",
        "amount": 1100.00,
        "status": "DELIVERED",
    },
]

print("=" * 72)
print("RELIABLE STREAMING PIPELINE - EVENT PRODUCER")
print("=" * 72)

for event in events:
    metadata = producer.send(
        TOPIC,
        value=event
    ).get(timeout=10)

    print(
        f"Published {event['order_id']} | "
        f"Partition: {metadata.partition} | "
        f"Offset: {metadata.offset}"
    )

    time.sleep(1)

producer.flush()
producer.close()

print("=" * 72)
print("All capstone events published successfully.")
print("=" * 72)