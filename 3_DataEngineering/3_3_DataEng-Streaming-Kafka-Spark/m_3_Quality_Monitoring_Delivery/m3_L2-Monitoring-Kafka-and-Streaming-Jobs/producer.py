import json
import time
from kafka import KafkaProducer

TOPIC = "monitoring-orders"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)

orders = [
    {"order_id": "MON001", "customer": "Asha", "amount": 1200.00},
    {"order_id": "MON002", "customer": "Rahul", "amount": 850.50},
    {"order_id": "MON003", "customer": "Meera", "amount": 2100.00},
    {"order_id": "MON004", "customer": "Vikram", "amount": 675.25},
    {"order_id": "MON005", "customer": "Neha", "amount": 1450.00},
    {"order_id": "MON006", "customer": "Arjun", "amount": 3200.50},
    {"order_id": "MON007", "customer": "Priya", "amount": 990.00},
    {"order_id": "MON008", "customer": "Karan", "amount": 1850.75},
]

print("=" * 68)
print("KAFKA MONITORING DEMO - EVENT PRODUCER")
print("=" * 68)

for order in orders:
    metadata = producer.send(TOPIC, value=order).get(timeout=10)

    print(
        f"Published {order['order_id']} | "
        f"Partition: {metadata.partition} | "
        f"Offset: {metadata.offset}"
    )

    time.sleep(1)

producer.flush()
producer.close()

print("=" * 68)
print("All monitoring events published successfully.")
print("=" * 68)