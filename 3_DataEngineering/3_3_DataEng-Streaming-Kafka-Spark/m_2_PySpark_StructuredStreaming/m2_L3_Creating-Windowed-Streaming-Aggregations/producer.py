import json
import time
from datetime import datetime, timezone
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

orders = [
    {"order_id": "WIN001", "customer": "Asha", "amount": 500.00},
    {"order_id": "WIN002", "customer": "Rahul", "amount": 850.00},
    {"order_id": "WIN003", "customer": "Meera", "amount": 1200.00},
    {"order_id": "WIN004", "customer": "Vikram", "amount": 650.00},
    {"order_id": "WIN005", "customer": "Neha", "amount": 1800.00},
]

print("=" * 65)
print("WINDOWED STREAMING PRODUCER")
print("=" * 65)

for order in orders:
    order["event_time"] = datetime.now(timezone.utc).isoformat()

    metadata = producer.send("orders", value=order).get(timeout=10)

    print(
        f"Published {order['order_id']} | "
        f"Amount: {order['amount']} | "
        f"Partition: {metadata.partition} | "
        f"Offset: {metadata.offset}"
    )

    time.sleep(3)

producer.flush()
producer.close()

print("=" * 65)
print("All windowed streaming events published successfully.")
print("=" * 65)