import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

events = [
    {
        "order_id": "VAL001",
        "customer": "Asha",
        "amount": 1250.50,
        "status": "CREATED",
    },
    {
        "order_id": "VAL002",
        "customer": "",
        "amount": 899.00,
        "status": "PAID",
    },
    {
        "order_id": "VAL003",
        "customer": "Meera",
        "amount": -250.00,
        "status": "CREATED",
    },
    {
        "order_id": "VAL004",
        "customer": "Vikram",
        "amount": 1750.00,
        "status": "UNKNOWN",
    },
    {
        "order_id": "VAL005",
        "customer": "Neha",
        "amount": 2100.00,
        "status": "SHIPPED",
    },
]

print("=" * 68)
print("STREAMING EVENT VALIDATION PRODUCER")
print("=" * 68)

for event in events:
    metadata = producer.send(
        "validation-orders",
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
print("All validation test events published successfully.")
print("=" * 68)