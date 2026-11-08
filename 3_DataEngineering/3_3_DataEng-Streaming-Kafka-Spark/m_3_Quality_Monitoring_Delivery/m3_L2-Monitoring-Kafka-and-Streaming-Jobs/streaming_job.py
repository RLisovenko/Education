import json
import time
from kafka import KafkaConsumer

TOPIC = "monitoring-orders"
GROUP_ID = "order-streaming-job"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    group_id=GROUP_ID,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

processed_count = 0
start_time = time.time()

print("=" * 72)
print("MONITORED STREAMING JOB")
print("=" * 72)
print(f"Topic          : {TOPIC}")
print(f"Consumer Group : {GROUP_ID}")
print("Job Status     : RUNNING")
print("Waiting for streaming events...")
print("Press Ctrl+C to stop.")
print("=" * 72)

try:
    for message in consumer:
        processed_count += 1
        elapsed = max(time.time() - start_time, 0.001)
        processing_rate = processed_count / elapsed

        order = message.value

        print()
        print(
            f"Processed {order['order_id']} | "
            f"Customer: {order['customer']} | "
            f"Amount: {order['amount']}"
        )

        print(
            f"Partition: {message.partition} | "
            f"Offset: {message.offset}"
        )

        print(
            f"Metrics -> Processed: {processed_count} | "
            f"Rate: {processing_rate:.2f} events/sec"
        )

except KeyboardInterrupt:
    elapsed = max(time.time() - start_time, 0.001)
    final_rate = processed_count / elapsed

    print()
    print("=" * 72)
    print("STREAMING JOB STOPPED")
    print(f"Processed Events : {processed_count}")
    print(f"Average Rate     : {final_rate:.2f} events/sec")
    print("Job Status       : STOPPED")
    print("=" * 72)

finally:
    consumer.close()