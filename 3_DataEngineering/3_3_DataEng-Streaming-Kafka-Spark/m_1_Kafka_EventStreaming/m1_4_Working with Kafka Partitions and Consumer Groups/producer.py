import json

from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    key_serializer=lambda key: key.encode("utf-8"),
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

orders = [
    ("customer-A", {"order_id": "PORD101", "customer": "Asha", "amount": 1200}),
    ("customer-B", {"order_id": "PORD102", "customer": "Rahul", "amount": 850}),
    ("customer-C", {"order_id": "PORD103", "customer": "Meera", "amount": 2100}),
    ("customer-A", {"order_id": "PORD104", "customer": "Asha", "amount": 640}),
    ("customer-B", {"order_id": "PORD105", "customer": "Rahul", "amount": 1750}),
    ("customer-C", {"order_id": "PORD106", "customer": "Meera", "amount": 990}),
]

print("=" * 70)
print("PARTITIONED KAFKA PRODUCER")
print("=" * 70)

for key, order in orders:
    future = producer.send(
        "partitioned-orders",
        key=key,
        value=order,
    )

    metadata = future.get(timeout=10)

    print(
        f"Sent {order['order_id']} | "
        f"Key: {key} | "
        f"Partition: {metadata.partition} | "
        f"Offset: {metadata.offset}"
    )

producer.flush()
producer.close()

print("=" * 70)
print("All partitioned order events published successfully.")
print("=" * 70)