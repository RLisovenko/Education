"""Publish realistic and deliberately problematic smart-meter events to Kafka."""
import argparse
import json
import time
import uuid
from datetime import datetime, timedelta, timezone

from config import BOOTSTRAP_HOST, TOPIC

METERS = [
    ("MTR-001", "north"), ("MTR-002", "SOUTH"),
    ("MTR-003", "East"), ("MTR-004", "west"),
    ("MTR-005", "North"), ("MTR-006", "South"),
]


def stamp(when):
    return when.replace(microsecond=0).isoformat()


def reading(event_id, meter_id, region, kwh, voltage, status, when):
    return {
        "event_id": event_id,
        "meter_id": meter_id,
        "region": region,
        "energy_usage_kwh": kwh,
        "voltage": voltage,
        "device_status": status,
        "event_timestamp": stamp(when),
    }


def generate(mode, count):
    now = datetime.now(timezone.utc)
    run = uuid.uuid4().hex[:8].upper()
    if mode == "baseline":
        events = []
        for i in range(8):
            meter, region = METERS[i % len(METERS)]
            events.append(reading(f"GP-{run}-{i+1:03d}", meter, region,
                                  round(2.5 + i * 2.7, 2), 218 + (i % 5) * 4,
                                  "ONLINE" if i != 6 else "MAINTENANCE",
                                  now - timedelta(seconds=20 - i * 2)))
        # Same business event with another Kafka offset: deliberate duplicate.
        events.append(dict(events[2]))
        events.extend([
            reading(f"GP-{run}-BAD1", "", "North", 5.0, 220, "ONLINE", now),
            reading(f"GP-{run}-BAD2", "MTR-003", "East", -3.0, 220, "ONLINE", now),
            reading(f"GP-{run}-BAD3", "MTR-004", "West", 6.0, 400, "BROKEN", now),
        ])
        return events
    if mode == "late":
        return [
            reading(f"GP-{run}-LATE", "MTR-002", "South", 4.0, 221,
                    "ONLINE", now - timedelta(seconds=45)),
            reading(f"GP-{run}-VERY-LATE", "MTR-005", "North", 4.0, 221,
                    "ONLINE", now - timedelta(minutes=15)),
        ]
    if mode == "advance":
        # Controlled TEST event: advances event-time watermark to finalize old windows.
        # Not intended as a normal production device event.
        return [reading(f"GP-{run}-ADVANCE", "MTR-001", "North", 1.0,
                        220, "ONLINE", now + timedelta(minutes=10))]
    if mode == "invalid":
        bad_timestamp = reading(f"GP-{run}-BADTIME", "MTR-003", "East", 5.0, 220, "ONLINE", now)
        bad_timestamp["event_timestamp"] = "not-a-timestamp"
        return [
            reading(f"GP-{run}-NOMETER", None, "South", 3.0, 220, "ONLINE", now),
            reading(f"GP-{run}-ZERO", "MTR-002", "South", -2.0, 220, "ONLINE", now),
            bad_timestamp,
            "{not-valid-json",
        ]
    return [
        reading(f"GP-{run}-{i+1:06d}", *METERS[i % len(METERS)],
                round(1.0 + (i % 20) * 0.7, 2), 215 + i % 20,
                "ONLINE", now + timedelta(milliseconds=i * 10))
        for i in range(count)
    ]


def main():
    from kafka import KafkaProducer
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["baseline", "late", "advance", "invalid", "burst"],
                        default="baseline")
    parser.add_argument("--count", type=int, default=200, help="For --mode burst")
    parser.add_argument("--interval", type=float, default=0.3, help="Seconds between sends")
    args = parser.parse_args()
    events = generate(args.mode, args.count)
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_HOST,
        key_serializer=lambda v: v.encode("utf-8"),
        value_serializer=lambda v: (v if isinstance(v, str) else json.dumps(v)).encode("utf-8"),
        acks="all", retries=5,
    )
    print(f"GridPulse Producer | topic={TOPIC} | mode={args.mode} | messages={len(events)}")
    try:
        for event in events:
            meter_id = event.get("meter_id") if isinstance(event, dict) else None
            event_id = event.get("event_id") if isinstance(event, dict) else "MALFORMED"
            # Stable meter key for ordering of events from the same device.
            metadata = producer.send(TOPIC, key=meter_id or "UNKNOWN-METER", value=event).get(timeout=15)
            print(f"Published {event_id} | key={meter_id or 'UNKNOWN-METER'} | "
                  f"partition={metadata.partition} | offset={metadata.offset}")
            if args.interval > 0:
                time.sleep(args.interval)
        producer.flush()
        print("Producer completed successfully.")
    finally:
        producer.close()


if __name__ == "__main__":
    main()
