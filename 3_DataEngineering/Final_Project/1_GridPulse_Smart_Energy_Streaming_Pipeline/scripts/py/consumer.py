"""Inspect Kafka event keys, values, partitions, offsets and group assignments."""
import argparse
from kafka import KafkaConsumer
from config import BOOTSTRAP_HOST, TOPIC


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", default="gridpulse-inspector")
    parser.add_argument("--max-messages", type=int, default=20)
    parser.add_argument("--timeout-ms", type=int, default=12000)
    parser.add_argument("--latest", action="store_true", help="Ignore old events for a new group")
    args = parser.parse_args()
    consumer = KafkaConsumer(
        TOPIC, bootstrap_servers=BOOTSTRAP_HOST, group_id=args.group,
        auto_offset_reset="latest" if args.latest else "earliest",
        enable_auto_commit=False, consumer_timeout_ms=args.timeout_ms,
        key_deserializer=lambda x: x.decode("utf-8") if x else None,
        value_deserializer=lambda x: x.decode("utf-8"),
    )
    print(f"Inspector | topic={TOPIC} | group={args.group}")
    received = 0
    try:
        for message in consumer:
            received += 1
            print(f"key={message.key} partition={message.partition} offset={message.offset} "
                  f"payload={message.value}")
            if received >= args.max_messages:
                break
        print(f"Messages inspected: {received}")
        print(f"Assigned partitions: {sorted(p.partition for p in consumer.assignment())}")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
