import time
from kafka import KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient

TOPIC = "monitoring-orders"
GROUP_ID = "order-streaming-job"
PARTITION = 0

admin = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
    client_id="monitoring-demo",
)

consumer = KafkaConsumer(
    bootstrap_servers="localhost:9092",
    enable_auto_commit=False,
)

topic_partition = TopicPartition(TOPIC, PARTITION)

print("=" * 68)
print("KAFKA CONSUMER MONITOR")
print("=" * 68)
print(f"Topic          : {TOPIC}")
print(f"Consumer Group : {GROUP_ID}")
print("Monitoring partition offsets and consumer lag.")
print("Press Ctrl+C to stop.")
print("=" * 68)

try:
    while True:
        latest_offset = consumer.end_offsets([topic_partition])[topic_partition]

        offsets = admin.list_consumer_group_offsets(GROUP_ID)

        committed = offsets.get(topic_partition)

        if committed is None:
            consumer_offset = 0
        else:
            consumer_offset = committed.offset

        lag = max(latest_offset - consumer_offset, 0)

        if lag == 0:
            status = "HEALTHY"
        elif lag <= 3:
            status = "PROCESSING"
        else:
            status = "LAGGING"

        print()
        print("-" * 68)
        print(f"Topic            : {TOPIC}")
        print(f"Partition        : {PARTITION}")
        print(f"Latest Offset    : {latest_offset}")
        print(f"Consumer Offset  : {consumer_offset}")
        print(f"Consumer Lag     : {lag}")
        print(f"Status           : {status}")
        print("-" * 68)

        time.sleep(3)

except KeyboardInterrupt:
    print()
    print("=" * 68)
    print("KAFKA MONITORING STOPPED")
    print("=" * 68)

finally:
    consumer.close()
    admin.close()