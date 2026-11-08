import json
import sys
from kafka import KafkaConsumer

TOPIC = "capstone-orders"
GROUP_ID = "reliable-streaming-pipeline"

FAILED_EVENT_FILE = "failed_event.json"
PROCESSED_FILE = "processed_orders.jsonl"

VALID_STATUSES = {
    "CREATED",
    "PAID",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
}

recovery_mode = "--recover" in sys.argv


def validate_event(event):
    errors = []

    if not event.get("order_id"):
        errors.append("order_id is required")

    customer = event.get("customer")

    if not customer or not str(customer).strip():
        errors.append("customer is required")

    amount = event.get("amount")

    if amount is None:
        errors.append("amount is required")
    elif not isinstance(amount, (int, float)):
        errors.append("amount must be numeric")
    elif amount <= 0:
        errors.append("amount must be greater than zero")

    status = event.get("status")

    if not status:
        errors.append("status is required")
    elif status not in VALID_STATUSES:
        errors.append(f"unsupported status: {status}")

    return errors


consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    group_id=GROUP_ID,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

processed_count = 0
rejected_count = 0

print("=" * 76)
print("RELIABLE OPEN-SOURCE STREAMING PIPELINE")
print("=" * 76)
print(f"Topic          : {TOPIC}")
print(f"Consumer Group : {GROUP_ID}")
print(f"Recovery Mode  : {'ON' if recovery_mode else 'OFF'}")
print("Pipeline Status: RUNNING")
print("=" * 76)

try:
    for message in consumer:
        event = message.value

        validation_errors = validate_event(event)

        if validation_errors:
            rejected_count += 1

            print()
            print("[REJECTED EVENT]")
            print(f"Order: {event.get('order_id')}")

            for error in validation_errors:
                print(f"Reason: {error}")

            print(
                f"Kafka Position -> "
                f"Partition: {message.partition} | "
                f"Offset: {message.offset}"
            )

            consumer.commit()
            continue

        try:
            if event.get("simulate_failure") and not recovery_mode:
                raise RuntimeError(
                    "Simulated processing failure for capstone recovery"
                )

            with open(
                PROCESSED_FILE,
                "a",
                encoding="utf-8"
            ) as file:
                file.write(json.dumps(event) + "\n")

            processed_count += 1

            print()
            print("[PROCESSED EVENT]")
            print(
                f"Order: {event.get('order_id')} | "
                f"Customer: {event.get('customer')} | "
                f"Amount: {event.get('amount')} | "
                f"Status: {event.get('status')}"
            )

            print(
                f"Kafka Position -> "
                f"Partition: {message.partition} | "
                f"Offset: {message.offset}"
            )

            print(
                f"Pipeline Metrics -> "
                f"Processed: {processed_count} | "
                f"Rejected: {rejected_count}"
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
            print("=" * 76)
            print("PIPELINE FAILURE DETECTED")
            print("=" * 76)
            print(f"Failed Event : {event.get('order_id')}")
            print(f"Partition    : {message.partition}")
            print(f"Offset       : {message.offset}")
            print(f"Reason       : {error}")
            print(f"Failure File : {FAILED_EVENT_FILE}")
            print("Pipeline Status: STOPPED")
            print("=" * 76)

            raise

except KeyboardInterrupt:
    print()
    print("Pipeline stopped manually.")

except Exception:
    pass

finally:
    consumer.close()