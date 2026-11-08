import json
import sys
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

first_batch = [
    {
        "order_id": "REC001",
        "customer": "Asha",
        "amount": 1250.50,
        "status": "CREATED",
    },
    {
        "order_id": "REC002",
        "customer": "Rahul",
        "amount": 899.00,
        "status": "PAID",
    },
    {
        "order_id": "REC003",
        "customer": "Meera",
        "amount": 2100.75,
        "status": "CREATED",
    },
]

second_batch = [
    {
        "order_id": "REC004",
        "customer": "Vikram",
        "amount": 1750.00,
        "status": "PAID",
    },
    {
        "order_id": "REC005",
        "customer": "Neha",
        "amount": 2450.25,
        "status": "SHIPPED",
    },
]

batch_name = sys.argv[1] if len(sys.argv) > 1 else "batch1"

if batch_name == "batch1":
    orders = first_batch
elif batch_name == "batch2":
    orders = second_batch
else:
    print("Usage: python producer.py batch1")
    print("   or: python producer.py batch2")
    sys.exit(1)

print("=" * 65)
print(f"CHECKPOINT RECOVERY PRODUCER - {batch_name.upper()}")
print("=" * 65)

for order in orders:
    metadata = producer.send(
        "checkpoint-orders",
        value=order
    ).get(timeout=10)

    print(
        f"Published {order['order_id']} | "
        f"Partition: {metadata.partition} | "
        f"Offset: {metadata.offset}"
    )

    time.sleep(2)

producer.flush()
producer.close()

print("=" * 65)
print(f"{batch_name.upper()} published successfully.")
print("=" * 65)