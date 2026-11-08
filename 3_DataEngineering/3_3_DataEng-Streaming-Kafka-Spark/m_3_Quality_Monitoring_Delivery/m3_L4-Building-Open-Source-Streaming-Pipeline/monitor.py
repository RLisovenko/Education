import time
from kafka import KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient

TOPIC = "capstone-orders"
GROUP_ID = "reliable-streaming-pipeline"
PARTITION = 0

admin = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
    client_id="capstone-monitor",
)

consumer = KafkaConsumer(
    bootstrap_servers="localhost:9092",
    enable_auto_commit=False,
)

topic_partition = TopicPartition(TOPIC, PARTITION)

print("=" * 72)
print("CAPSTONE STREAMING PIPELINE MONITOR")
print("=" * 72)
print(f"Topic          : {TOPIC}")
print(f"Consumer Group : {GROUP_ID}")
print("Press Ctrl+C to stop.")
print("=" * 72)

try:
    while True:
        latest_offset = consumer.end_offsets(
            [topic_partition]
        )[topic_partition]

        offsets = admin.list_consumer_group_offsets(
            GROUP_ID
        )

        committed = offsets.get(topic_partition)

        consumer_offset = (
            committed.offset
            if committed is not None
            else 0
        )

        lag = max(
            latest_offset - consumer_offset,
            0
        )

        if lag == 0:
            status = "HEALTHY"
        elif lag <= 2:
            status = "RECOVERING"
        else:
            status = "LAGGING"

        print()
        print("-" * 72)
        print(f"Latest Offset   : {latest_offset}")
        print(f"Consumer Offset : {consumer_offset}")
        print(f"Consumer Lag    : {lag}")
        print(f"Pipeline Status : {status}")
        print("-" * 72)

        time.sleep(3)

except KeyboardInterrupt:
    print()
    print("Monitoring stopped.")

finally:
    consumer.close()
    admin.close()