import json
import os
import sys
from kafka import KafkaConsumer
from kafka.structs import TopicPartition

TOPIC = "failure-orders"
GROUP_ID = "failure-recovery-pipeline"
FAILED_EVENT_FILE = "failed_event.json"

recovery_mode = "--recover" in sys.argv

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    group_id=GROUP_ID,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

print("=" * 72)
print("FAILURE-AWARE STREAMING PIPELINE")
print("=" * 72)
print(f"Topic          : {TOPIC}")
print(f"Consumer Group : {GROUP_ID}")
print(f"Recovery Mode  : {'ON' if recovery_mode else 'OFF'}")
print("Pipeline Status: RUNNING")
print("Press Ctrl+C to stop.")
print("=" * 72)

processed_count = 0

try:
    for message in consumer:
        event = message.value

        try:
            if event.get("simulate_failure") and not recovery_mode:
                raise RuntimeError(
                    "Simulated processing failure for demonstration"
                )

            processed_count += 1

            print()
            print(
                f"Processed {event.get('order_id')} | "
                f"Customer: {event.get('customer')} | "
                f"Amount: {event.get('amount')} | "
                f"Status: {event.get('status')}"
            )

            print(
                f"Kafka Position -> "
                f"Partition: {message.partition} | "
                f"Offset: {message.offset}"
            )

            consumer.commit()

        except Exception as error:
            failure_record = {
                "event": event,
                "topic": message.topic,
                "partition": message.partition,
                "offset": message.offset,
                "error": str(error),
            }

            with open(
                FAILED_EVENT_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    failure_record,
                    file,
                    indent=2
                )

            print()
            print("=" * 72)
            print("PIPELINE FAILURE DETECTED")
            print("=" * 72)
            print(f"Failed Event : {event.get('order_id')}")
            print(f"Partition    : {message.partition}")
            print(f"Offset       : {message.offset}")
            print(f"Reason       : {error}")
            print(f"Failure saved to: {FAILED_EVENT_FILE}")
            print("Pipeline Status: STOPPED")
            print("=" * 72)

            raise

except KeyboardInterrupt:
    print()
    print("Pipeline stopped manually.")

except Exception:
    pass

finally:
    consumer.close()