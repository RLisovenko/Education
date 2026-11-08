import json
import time
from kafka import KafkaProducer

TOPIC = "failure-orders"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

events = [
    {
        "order_id": "FAIL001",
        "customer": "Asha",
        "amount": 1200.00,
        "status": "CREATED",
    },
    {
        "order_id": "FAIL002",
        "customer": "Rahul",
        "amount": 850.50,
        "status": "PAID",
    },
    {
        "order_id": "FAIL003",
        "customer": "Meera",
        "amount": -999.00,
        "status": "CREATED",
        "simulate_failure": True,
    },
    {
        "order_id": "FAIL004",
        "customer": "Vikram",
        "amount": 1750.00,
        "status": "PAID",
    },
    {
        "order_id": "FAIL005",
        "customer": "Neha",
        "amount": 2450.25,
        "status": "SHIPPED",
    },
]

print("=" * 68)
print("FAILURE HANDLING DEMO - EVENT PRODUCER")
print("=" * 68)

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

print("=" * 68)
print("All failure-test events published successfully.")
print("=" * 68)