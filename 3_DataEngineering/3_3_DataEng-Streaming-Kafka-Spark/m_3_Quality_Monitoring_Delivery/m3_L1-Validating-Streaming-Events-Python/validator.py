from kafka import KafkaConsumer

VALID_STATUSES = {
    "CREATED",
    "PAID",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
}


def validate_event(event):
    errors = []

    order_id = event.get("order_id")
    customer = event.get("customer")
    amount = event.get("amount")
    status = event.get("status")

    if not order_id:
        errors.append("order_id is required")

    if not customer or not str(customer).strip():
        errors.append("customer is required")

    if amount is None:
        errors.append("amount is required")
    elif not isinstance(amount, (int, float)):
        errors.append("amount must be numeric")
    elif amount <= 0:
        errors.append("amount must be greater than zero")

    if not status:
        errors.append("status is required")
    elif status not in VALID_STATUSES:
        errors.append(f"unsupported status: {status}")

    return errors


consumer = KafkaConsumer(
    "validation-orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda value: __import__("json").loads(
        value.decode("utf-8")
    ),
)

print("=" * 72)
print("PYTHON STREAMING EVENT VALIDATOR")
print("=" * 72)
print("Listening for events from topic: validation-orders")
print("Press Ctrl+C to stop.")
print("=" * 72)

valid_count = 0
invalid_count = 0

try:
    for message in consumer:
        event = message.value
        errors = validate_event(event)

        print()

        if not errors:
            valid_count += 1

            print("[VALID EVENT]")
            print(
                f"Order: {event.get('order_id')} | "
                f"Customer: {event.get('customer')} | "
                f"Amount: {event.get('amount')} | "
                f"Status: {event.get('status')}"
            )
        else:
            invalid_count += 1

            print("[INVALID EVENT]")
            print(f"Order: {event.get('order_id')}")

            for error in errors:
                print(f"Reason: {error}")

        print(
            f"Kafka Position -> "
            f"Partition: {message.partition} | "
            f"Offset: {message.offset}"
        )

        print(
            f"Validation Summary -> "
            f"Valid: {valid_count} | "
            f"Invalid: {invalid_count}"
        )

except KeyboardInterrupt:
    print()
    print("=" * 72)
    print("VALIDATION SESSION STOPPED")
    print(
        f"Final Summary -> "
        f"Valid: {valid_count} | "
        f"Invalid: {invalid_count}"
    )
    print("=" * 72)

finally:
    consumer.close()